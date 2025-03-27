#!/bin/bash

export PGPASSWORD=$DB_PASSWORD
if [ -f dump.bin ]; then
    # If $DB_HOST and $DB_PORT are not set, the command will use the default values.
    # If $DB_HOST and $DB_PORT are set, the command will use the provided values.
    # Cool for running inside and outside of a container.
    PG_RESTORE_CMD="pg_restore -j 8 -F c -U $DB_USER -d $DB_NAME --no-privileges --no-owner dump.bin"
    if [ -n "$DB_HOST" ]; then
        PG_RESTORE_CMD="$PG_RESTORE_CMD -h $DB_HOST"
    fi
    if [ -n "$DB_PORT" ]; then
        PG_RESTORE_CMD="$PG_RESTORE_CMD -p $DB_PORT"
    fi

    $PG_RESTORE_CMD

    if [ $? -eq 0 ]; then
        echo "Restore completed successfully."
    else
        echo "Restore failed."
    fi
else
    echo "dump.bin does not exist."
fi