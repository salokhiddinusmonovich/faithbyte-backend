#!/usr/bin/env bash

BACKUP_DIR_PATH='/backups'
BACKUP_FILE_PREFIX='backup'


# forming the name`s file with dates
backup_filename="${BACKUP_DIR_PATH}/${BACKUP_FILE_PREFIX}_$(data + '%Y%M%d').sql.gz"

