



if [ $INIT_TYPE -eq 1 ]; then
    alembic upgrade head
    alembic revision --autogenerate -m $UPDATE_NAME
    alembic upgrade head
elif [ $INIT_TYPE -eq 0 ]; then
    alembic upgrade $REVISION_ID
else
    alembic downgrade $REVISION_ID
fi


