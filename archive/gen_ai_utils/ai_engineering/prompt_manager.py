"""Prompt Management - Template system for LLM prompts"""

from typing import Dict, Any, List, Optional
from pathlib import Path
import json
import yaml


class PromptTemplate:
    """Prompt template with variable substitution"""

    def __init__(self, template: str, variables: Optional[List[str]] = None):
        self.template = template
        self.variables = variables or []

    def format(self, **kwargs) -> str:
        """Format template with variables"""
        return self.template.format(**kwargs)

    def to_dict(self) -> Dict[str, Any]:
        return {'template': self.template, 'variables': self.variables}


class PromptManager:
    """Manage and version prompts"""

    def __init__(self):
        self.prompts: Dict[str, PromptTemplate] = {}

    def add(self, name: str, template: str, variables: Optional[List[str]] = None):
        """Add a prompt template"""
        self.prompts[name] = PromptTemplate(template, variables)

    def get(self, name: str) -> Optional[PromptTemplate]:
        """Get a prompt template"""
        return self.prompts.get(name)

    def format(self, name: str, **kwargs) -> str:
        """Format a prompt with variables"""
        template = self.get(name)
        if not template:
            raise ValueError(f"Prompt '{name}' not found")
        return template.format(**kwargs)

    def save(self, filepath: str):
        """Save prompts to file"""
        data = {name: template.to_dict() for name, template in self.prompts.items()}
        path = Path(filepath)

        if path.suffix == '.json':
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
        elif path.suffix in ['.yml', '.yaml']:
            with open(filepath, 'w') as f:
                yaml.dump(data, f)

    def load(self, filepath: str):
        """Load prompts from file"""
        path = Path(filepath)

        if path.suffix == '.json':
            with open(filepath, 'r') as f:
                data = json.load(f)
        elif path.suffix in ['.yml', '.yaml']:
            with open(filepath, 'r') as f:
                data = yaml.safe_load(f)

        for name, info in data.items():
            self.add(name, info['template'], info.get('variables'))


def load_prompts(filepath: str) -> PromptManager:
    """Load prompts from file"""
    manager = PromptManager()
    manager.load(filepath)
    return manager
