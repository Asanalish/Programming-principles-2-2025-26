DROP PROCEDURE IF EXISTS pb_add_or_update(TEXT, TEXT);
DROP PROCEDURE IF EXISTS pb_add_many(TEXT[], TEXT[]);
DROP PROCEDURE IF EXISTS pb_delete(TEXT, TEXT);

CREATE PROCEDURE pb_add_or_update(p_name TEXT, p_phone TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM pb_contacts WHERE person_name = p_name) THEN
        UPDATE pb_contacts SET phone = p_phone WHERE person_name = p_name;
    ELSE
        INSERT INTO pb_contacts(person_name, phone)
        VALUES (p_name, p_phone);
    END IF;
END;
$$;


CREATE PROCEDURE pb_add_many(p_names TEXT[], p_phones TEXT[])
LANGUAGE plpgsql
AS $$
DECLARE
    i INT;
BEGIN
    CREATE TEMP TABLE IF NOT EXISTS pb_invalid_data (
        bad_name TEXT,
        bad_phone TEXT
    ) ON COMMIT PRESERVE ROWS;

    DELETE FROM pb_invalid_data;

    FOR i IN 1..array_length(p_names, 1) LOOP
        IF p_phones[i] ~ '^\\+?[0-9]{10,15}$' THEN
            CALL pb_add_or_update(p_names[i], p_phones[i]);
        ELSE
            INSERT INTO pb_invalid_data VALUES (p_names[i], p_phones[i]);
        END IF;
    END LOOP;
END;
$$;


CREATE PROCEDURE pb_delete(p_name TEXT DEFAULT NULL, p_phone TEXT DEFAULT NULL)
LANGUAGE plpgsql
AS $$
BEGIN
    IF p_phone IS NOT NULL THEN
        DELETE FROM pb_contacts WHERE phone = p_phone;
    ELSIF p_name IS NOT NULL THEN
        DELETE FROM pb_contacts WHERE person_name = p_name;
    END IF;
END;
$$;