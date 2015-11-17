-- Adapted from https://wiki.postgresql.org/wiki/Audit_trigger_91plus

CREATE EXTENSION IF NOT EXISTS hstore;
 
CREATE SCHEMA IF NOT EXISTS audit;
REVOKE ALL ON SCHEMA audit FROM public;

CREATE TABLE IF NOT EXISTS audit.action_log(
  id bigserial PRIMARY KEY,
  transaction_id BIGINT,
  action_timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
  table_name text NOT NULL,
  row_id BIGINT,
  app_user_id BIGINT,
  action CHAR(1) NOT NULL CHECK (action IN ('I', 'D', 'U', 'T')),
  row_data hstore,
  changed_fields hstore
);
 
REVOKE ALL ON audit.logged_actions FROM public;


CREATE OR REPLACE FUNCTION audit.if_modified_func() RETURNS TRIGGER AS $body$
DECLARE
  audit_row action_log;
  include_values BOOLEAN;
  log_diffs BOOLEAN;
  h_old hstore;
  h_new hstore;
  excluded_cols text[] = ARRAY[]::text[];
BEGIN

  audit_row.id = NEXTVAL('action_log_id_seq');
  audit_row.transaction_id = txid_current();
  audit_row.action_timestamp = CURRENT_TIMESTAMP;
  audit_row.table_name = TG_TABLE_NAME::text;
  IF (TG_LEVEL = 'ROW') THEN
    IF (TG_OP='DELETE') THEN
      audit_row.row_id = OLD.id;
      audit_row.app_user_id = coalesce(OLD.last_modified_by_id, OLD.created_by_id);
    ELSE
      audit_row.row_id = NEW.id;
      audit_row.app_user_id = coalesce(NEW.last_modified_by_id, NEW.created_by_id);
    END IF;
  END IF;
  audit_row.action = SUBSTRING(TG_OP,1,1);
 
  IF TG_ARGV[1] IS NOT NULL THEN
    excluded_cols = TG_ARGV[1]::text[];
  END IF;
 
  IF (TG_OP = 'UPDATE' AND TG_LEVEL = 'ROW') THEN
    audit_row.row_data = hstore(OLD.*);
    audit_row.changed_fields =  (hstore(NEW.*) - audit_row.row_data) - excluded_cols;
    IF audit_row.changed_fields = hstore('') THEN
      -- All changed fields are ignored. Skip this update.
      RETURN NULL;
    END IF;
  ELSIF (TG_OP = 'DELETE' AND TG_LEVEL = 'ROW') THEN
    audit_row.row_data = hstore(OLD.*) - excluded_cols;
  ELSIF (TG_OP = 'INSERT' AND TG_LEVEL = 'ROW') THEN
    audit_row.row_data = hstore(NEW.*) - excluded_cols;
  ELSE
    RAISE EXCEPTION '[audit.if_modified_func] - Trigger func added as trigger for unhandled case: %, %',TG_OP, TG_LEVEL;
    RETURN NULL;
  END IF;
  INSERT INTO action_log (
    id,
    transaction_id,
    action_timestamp,
    table_name,
    row_id,
    app_user_id,
    action,
    row_data,
    changed_fields
  ) VALUES (
    audit_row.id,
    audit_row.transaction_id,
    audit_row.action_timestamp,
    audit_row.table_name,
    audit_row.row_id,
    audit_row.app_user_id,
    audit_row.action,
    audit_row.row_data,
    audit_row.changed_fields
  );
  RETURN NULL;
END;
$body$
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = pg_catalog, public;
  
CREATE OR REPLACE FUNCTION audit.audit_table(target_table regclass, audit_rows BOOLEAN, audit_query_text BOOLEAN, ignored_cols text[]) RETURNS void AS $body$
DECLARE
  stm_targets text = 'INSERT OR UPDATE OR DELETE OR TRUNCATE';
  _q_txt text;
  _ignored_cols_snip text = '';
BEGIN
    EXECUTE 'DROP TRIGGER IF EXISTS audit_trigger_row ON ' || quote_ident(target_table::text);
    EXECUTE 'DROP TRIGGER IF EXISTS audit_trigger_stm ON ' || quote_ident(target_table::text);
 
    IF audit_rows THEN
        IF array_length(ignored_cols,1) > 0 THEN
            _ignored_cols_snip = ', ' || quote_literal(ignored_cols);
        END IF;
        _q_txt = 'CREATE TRIGGER audit_trigger_row AFTER INSERT OR UPDATE OR DELETE ON ' || 
                 quote_ident(target_table::text) || 
                 ' FOR EACH ROW EXECUTE PROCEDURE audit.if_modified_func(' ||
                 quote_literal(audit_query_text) || _ignored_cols_snip || ');';
        RAISE NOTICE '%',_q_txt;
        EXECUTE _q_txt;
        stm_targets = 'TRUNCATE';
    ELSE
    END IF;
 
    _q_txt = 'CREATE TRIGGER audit_trigger_stm AFTER ' || stm_targets || ' ON ' ||
             quote_ident(target_table::text) ||
             ' FOR EACH STATEMENT EXECUTE PROCEDURE audit.if_modified_func('||
             quote_literal(audit_query_text) || ');';
    RAISE NOTICE '%',_q_txt;
    EXECUTE _q_txt;
 
END;
$body$
LANGUAGE 'plpgsql';
 
-- Pg doesn't allow variadic calls with 0 params, so provide a wrapper
CREATE OR REPLACE FUNCTION audit.audit_table(target_table regclass, audit_rows BOOLEAN, audit_query_text BOOLEAN) RETURNS void AS $body$
SELECT audit.audit_table($1, $2, $3, ARRAY[]::text[]);
$body$ LANGUAGE SQL;
 
-- And provide a convenience call wrapper for the simplest case
-- of row-level logging with no excluded cols and query logging enabled.
--
CREATE OR REPLACE FUNCTION audit.audit_table(target_table regclass) RETURNS void AS $$
SELECT audit.audit_table($1, BOOLEAN 't', BOOLEAN 't');
$$ LANGUAGE 'sql';

CREATE SCHEMA IF NOT EXISTS audit;

SELECT
  audit.audit_table(table_name)
FROM
  information_schema.tables
WHERE
  table_schema = 'public'
  AND table_name != 'alembic_version'
  AND table_name != 'action_log'