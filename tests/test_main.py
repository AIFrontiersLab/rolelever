"""Tests for TextProcessor MVP."""
import pytest
from main import Agent, ProcessRequest, ProcessResponse, app, demo
from fastapi.testclient import TestClient

client = TestClient(app)

class TestAgent:
    def test_agent_initialization(self):
        agent = Agent("test")
        assert agent.name == "test"
        assert isinstance(agent.cache, dict)

    def test_agent_execute(self):
        agent = Agent("test")
        res = agent.execute("hello", "uppercase")
        assert res == "HELLO"
        res2 = agent.execute("HELLO", "lowercase")
        assert res2 == "hello"
        res3 = agent.execute("abc", "reverse")
        assert res3 == "cba"

class TestProcess:
    def test_process_empty_agents(self):
        agent = Agent("empty")
        assert len(agent.cache) == 0

    def test_process_failure_handling(self):
        agent = Agent("fail")
        with pytest.raises(ValueError):
            agent.execute("test", "invalid_op")

    def test_process_initialization(self):
        agent = Agent("init")
        assert agent.name == "init"

    def test_process_sequential_execution(self):
        agent = Agent("seq")
        r1 = agent.execute("a", "uppercase")
        r2 = agent.execute("a", "uppercase")
        assert r1 == r2
        assert len(agent.cache) == 1  # Cached

class TestDemo:
    def test_demo_function(self):
        result = demo()
        assert isinstance(result, str)
        assert len(result) > 0

    def test_demo_output_content(self):
        result = demo()
        assert "Final Output" in result
        assert "HELLO WORLD" in result

class TestAPI:
    def test_api_happy_path(self):
        resp = client.post("/process", json={"text": "hello", "operation": "uppercase"})
        assert resp.status_code == 200
        data = resp.json()
        assert data["result"] == "HELLO"
        assert data["length"] == 5

    def test_api_failure_path(self):
        resp = client.post("/process", json={"text": "hello", "operation": "bad"})
        assert resp.status_code == 400
