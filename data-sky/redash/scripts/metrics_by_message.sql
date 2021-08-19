\set options '{"parameters": [{"value": "':field'", "type": "text", "name": "metric", "locals": [], "title": "metric", "global": false},{"value": "':message'", "type": "text", "name": "message", "locals": [], "title": "message"}]}'
\set message_with_time :message'_':now

INSERT INTO queries (updated_at, created_at, VERSION, org_id, data_source_id, latest_query_data_id, name, description, query, query_hash, api_key, user_id, last_modified_by_id, is_archived, is_draft, schedule, schedule_failures, OPTIONS, search_vector, tags)
SELECT q.updated_at,
       q.created_at,
       q.version,
       q.org_id,
       d.last_value,
       q.latest_query_data_id,
       concat(substring(q.name from '#"% #"%' for '#'),:'field'),
       q.description,
       q.query,
       q.query_hash,
       q.api_key,
       q.user_id,
       q.last_modified_by_id,
       q.is_archived,
       q.is_draft,
       q.schedule,
       q.schedule_failures,
       :'options',
       q.search_vector,
       array[:'message_with_time']
FROM queries q,
     data_sources_id_seq d
WHERE 'for_each_metrics'=ANY(q.tags)
ORDER BY q.id;

INSERT INTO visualizations (updated_at, created_at, TYPE, query_id, name, description, OPTIONS)
SELECT v.updated_at,
       v.created_at,
       v.type,
       q.new_id,
       v.name,
       v.description,
       v.options
FROM
  (SELECT ins.id AS new_id,
          qu.id AS example_id
   FROM queries ins
   JOIN
     (SELECT *
      FROM queries
      WHERE 'for_each_metrics'=ANY(tags)) qu ON ins.updated_at=qu.updated_at
   AND ins.created_at=qu.created_at
   WHERE ins.name like concat('%',:'field') AND ins.tags::text[]=array[:'message_with_time']) q
JOIN visualizations v ON q.example_id=v.query_id
ORDER BY q.example_id;


INSERT INTO widgets (updated_at, created_at, visualization_id,text,width, OPTIONS, dashboard_id)
SELECT w.updated_at,
       w.created_at,
       w.new_id,
       w.text,
       w.width,
       w.options,
       d.last_value
FROM
  dashboards_id_seq d,
  (SELECT *
   FROM
     (SELECT vi.id AS example_id,
             v.id AS new_id
      FROM
        (SELECT *
         FROM visualizations
         WHERE query_id IN
             (SELECT id
              FROM queries
              WHERE name like concat('%',:'field') AND tags::text[]=array[:'message_with_time'])) v
      JOIN
        (SELECT *
         FROM visualizations
         WHERE query_id IN
             (SELECT id
              FROM queries
              WHERE 'for_each_metrics'=ANY(tags))) vi ON vi.updated_at=v.updated_at
      AND vi.created_at=v.created_at
      WHERE v.id!=vi.id) vis
   JOIN widgets ON widgets.visualization_id=vis.example_id) w;