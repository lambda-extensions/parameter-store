
cd handler
poetry export -f requirements.txt --output requirements.txt
pip install -r requirements.txt -t .
cd ..

cd infrastructure
npx cdk deploy
