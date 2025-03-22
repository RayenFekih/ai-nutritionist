APP_PATH = src/ai_nutritionist/interfaces

clean: # clean dependencies and coverage report
	@echo ">> cleaning files"
	@rm -rf .venv htmlcov .qodo .ruff_cache .langgraph_api __pycache__

install: # install dependencies in the devcontainer
	@echo ">> installing dependencies"
	@poetry install

test: # run the unit tests
	@echo ">> running unit tests (Pytest)"
	@poetry run pytest

coverage: # generates test coverage report 
	@echo ">>> running coverage pytest"
	@poetry run pytest tests --cov=src --cov-report=html

run-ui: # run the streamlit chatbot app
	@echo ">> running the Streamlit app"
	@streamlit run ${APP_PATH}/streamlit_app.py

run-graph: #run the langgraph studio to interact with graph
	@echo ">> running the langgraph studio app"
	@langgraph dev