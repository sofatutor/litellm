#!/bin/sh

# Run database migrations first if enabled
if [ "$USE_PRISMA_MIGRATE" = "true" ] || [ "$USE_PRISMA_MIGRATE" = "True" ]; then
    echo "Running database migrations..."
    litellm --use_prisma_migrate
    echo "Database migrations completed."
fi

# Then start the main application
if [ "$USE_DDTRACE" = "true" ]; then
    export DD_TRACE_OPENAI_ENABLED="False"
    exec ddtrace-run litellm "$@"
else
    exec litellm "$@"
fi