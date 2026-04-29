CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_phone VARCHAR,
    p_type VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_contact_id INTEGER;
BEGIN
    SELECT id INTO v_contact_id
    FROM contacts
    WHERE LOWER(name) = LOWER(p_contact_name);

    IF v_contact_id IS NULL THEN
        RAISE NOTICE 'Contact not found: %', p_contact_name;
        RETURN;
    END IF;

    IF p_type NOT IN ('home', 'work', 'mobile') THEN
        RAISE NOTICE 'Wrong phone type. Use home, work, or mobile.';
        RETURN;
    END IF;

    INSERT INTO phones (contact_id, phone, type)
    VALUES (v_contact_id, p_phone, p_type);
END;
$$;


CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_contact_id INTEGER;
    v_group_id INTEGER;
BEGIN
    SELECT id INTO v_contact_id
    FROM contacts
    WHERE LOWER(name) = LOWER(p_contact_name);

    IF v_contact_id IS NULL THEN
        RAISE NOTICE 'Contact not found: %', p_contact_name;
        RETURN;
    END IF;

    INSERT INTO groups (name)
    VALUES (p_group_name)
    ON CONFLICT (name) DO NOTHING;

    SELECT id INTO v_group_id
    FROM groups
    WHERE LOWER(name) = LOWER(p_group_name);

    UPDATE contacts
    SET group_id = v_group_id
    WHERE id = v_contact_id;
END;
$$;


CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE (
    contact_id INTEGER,
    name VARCHAR,
    email VARCHAR,
    birthday DATE,
    group_name VARCHAR,
    phones TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        c.id AS contact_id,
        c.name,
        c.email,
        c.birthday,
        g.name AS group_name,
        COALESCE(STRING_AGG(p.phone || ' (' || p.type || ')', ', '), '') AS phones
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.id
    LEFT JOIN phones p ON p.contact_id = c.id
    GROUP BY c.id, c.name, c.email, c.birthday, g.name
    HAVING
        LOWER(c.name) LIKE LOWER('%' || p_query || '%')
        OR LOWER(COALESCE(c.email, '')) LIKE LOWER('%' || p_query || '%')
        OR LOWER(COALESCE(g.name, '')) LIKE LOWER('%' || p_query || '%')
        OR LOWER(COALESCE(STRING_AGG(p.phone, ', '), '')) LIKE LOWER('%' || p_query || '%');
END;
$$;


CREATE OR REPLACE FUNCTION get_contacts_page(
    p_limit INTEGER,
    p_offset INTEGER,
    p_sort_by TEXT
)
RETURNS TABLE (
    contact_id INTEGER,
    name VARCHAR,
    email VARCHAR,
    birthday DATE,
    group_name VARCHAR,
    date_added TIMESTAMP,
    phones TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        c.id AS contact_id,
        c.name,
        c.email,
        c.birthday,
        g.name AS group_name,
        c.date_added,
        COALESCE(STRING_AGG(p.phone || ' (' || p.type || ')', ', '), '') AS phones
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.id
    LEFT JOIN phones p ON p.contact_id = c.id
    GROUP BY c.id, c.name, c.email, c.birthday, g.name, c.date_added
    ORDER BY
        CASE WHEN p_sort_by = 'name' THEN c.name END ASC,
        CASE WHEN p_sort_by = 'birthday' THEN c.birthday END ASC,
        CASE WHEN p_sort_by = 'date_added' THEN c.date_added END ASC,
        c.id ASC
    LIMIT p_limit OFFSET p_offset;
END;
$$;