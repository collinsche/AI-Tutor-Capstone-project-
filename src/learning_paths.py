#!/usr/bin/env python3
"""
Personalized Learning Paths Generator
Generates customized curricula based on user profiles with adaptive difficulty
"""

import json
import random
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict

# Import EducationalAssistant with error handling
try:
    from .educational_assistant import EducationalAssistant
except ImportError:
    from educational_assistant import EducationalAssistant

@dataclass
class LearningModule:
    """Represents a single learning module"""
    id: str
    title: str
    description: str
    subject: str
    difficulty: int  # 1-5 scale
    prerequisites: List[str]
    estimated_time: int  # minutes
    content_type: str  # "lesson", "quiz", "project", "practice"
    topics: List[str]
    learning_objectives: List[str]

@dataclass
class LearningPath:
    """Represents a complete learning path"""
    id: str
    title: str
    description: str
    user_id: str
    subject: str
    modules: List[LearningModule]
    total_estimated_time: int
    difficulty_progression: List[int]
    created_at: datetime
    last_updated: datetime

class LearningPathGenerator:
    """Generates personalized learning paths based on user profiles"""
    
    def __init__(self):
        self.assistant = EducationalAssistant()
        self.module_library = self._initialize_module_library()
        
    def _initialize_module_library(self) -> Dict[str, List[LearningModule]]:
        """Initialize the library of available learning modules"""
        return {
            "Python Programming": [
                LearningModule(
                    id="py_basics_1",
                    title="Python Fundamentals",
                    description="Introduction to Python syntax, variables, and data types",
                    subject="Python Programming",
                    difficulty=1,
                    prerequisites=[],
                    estimated_time=45,
                    content_type="lesson",
                    topics=["variables", "data types", "basic syntax"],
                    learning_objectives=["Understand Python syntax", "Work with variables", "Use basic data types"]
                ),
                LearningModule(
                    id="py_control_1",
                    title="Control Structures",
                    description="Learn about if statements, loops, and conditional logic",
                    subject="Python Programming",
                    difficulty=2,
                    prerequisites=["py_basics_1"],
                    estimated_time=60,
                    content_type="lesson",
                    topics=["if statements", "for loops", "while loops", "conditional logic"],
                    learning_objectives=["Use conditional statements", "Implement loops", "Control program flow"]
                ),
                LearningModule(
                    id="py_functions_1",
                    title="Functions and Modules",
                    description="Creating and using functions, understanding scope",
                    subject="Python Programming",
                    difficulty=3,
                    prerequisites=["py_control_1"],
                    estimated_time=75,
                    content_type="lesson",
                    topics=["functions", "parameters", "return values", "scope", "modules"],
                    learning_objectives=["Define functions", "Use parameters and return values", "Understand scope"]
                ),
                LearningModule(
                    id="py_data_structures_1",
                    title="Data Structures",
                    description="Working with lists, dictionaries, sets, and tuples",
                    subject="Python Programming",
                    difficulty=3,
                    prerequisites=["py_functions_1"],
                    estimated_time=90,
                    content_type="lesson",
                    topics=["lists", "dictionaries", "sets", "tuples", "data manipulation"],
                    learning_objectives=["Use Python data structures", "Manipulate collections", "Choose appropriate data types"]
                ),
                LearningModule(
                    id="py_oop_1",
                    title="Object-Oriented Programming",
                    description="Classes, objects, inheritance, and polymorphism",
                    subject="Python Programming",
                    difficulty=4,
                    prerequisites=["py_data_structures_1"],
                    estimated_time=120,
                    content_type="lesson",
                    topics=["classes", "objects", "inheritance", "polymorphism", "encapsulation"],
                    learning_objectives=["Create classes and objects", "Implement inheritance", "Use OOP principles"]
                ),
                LearningModule(
                    id="py_quiz_1",
                    title="Python Basics Quiz",
                    description="Test your understanding of Python fundamentals",
                    subject="Python Programming",
                    difficulty=1,
                    prerequisites=["py_basics_1"],
                    estimated_time=20,
                    content_type="quiz",
                    topics=["variables", "data types", "basic syntax"],
                    learning_objectives=["Assess Python basics knowledge"]
                ),
                LearningModule(
                    id="py_project_1",
                    title="Calculator Project",
                    description="Build a simple calculator using Python",
                    subject="Python Programming",
                    difficulty=2,
                    prerequisites=["py_control_1"],
                    estimated_time=180,
                    content_type="project",
                    topics=["functions", "user input", "arithmetic operations"],
                    learning_objectives=["Apply Python concepts", "Build a complete program", "Handle user input"]
                )
            ],
            "Mathematics": [
                LearningModule(
                    id="math_algebra_1",
                    title="Algebra Fundamentals",
                    description="Basic algebraic operations and equations",
                    subject="Mathematics",
                    difficulty=2,
                    prerequisites=[],
                    estimated_time=60,
                    content_type="lesson",
                    topics=["variables", "equations", "algebraic operations"],
                    learning_objectives=["Solve basic equations", "Understand algebraic notation", "Manipulate expressions"]
                ),
                LearningModule(
                    id="math_geometry_1",
                    title="Geometry Basics",
                    description="Shapes, angles, and geometric relationships",
                    subject="Mathematics",
                    difficulty=2,
                    prerequisites=[],
                    estimated_time=75,
                    content_type="lesson",
                    topics=["shapes", "angles", "area", "perimeter"],
                    learning_objectives=["Calculate area and perimeter", "Understand geometric relationships", "Work with angles"]
                )
            ],
            "Computer Science": [
                LearningModule(
                    id="cs_algorithms_1",
                    title="Algorithm Fundamentals",
                    description="Introduction to algorithms and problem-solving",
                    subject="Computer Science",
                    difficulty=3,
                    prerequisites=[],
                    estimated_time=90,
                    content_type="lesson",
                    topics=["algorithms", "problem solving", "complexity"],
                    learning_objectives=["Understand algorithms", "Analyze complexity", "Solve problems systematically"]
                )
            ]
        }
    
    def generate_learning_path(self, user_profile: Dict[str, Any], subject: str, 
                             target_difficulty: Optional[int] = None) -> LearningPath:
        """Generate a personalized learning path for a user"""
        
        # Get user's current knowledge level and preferences
        knowledge_level = user_profile.get('knowledge_level', {}).get(subject, 1)
        learning_style = user_profile.get('learning_style', 'Visual')
        available_time = user_profile.get('available_time', 60)  # minutes per session
        goals = user_profile.get('goals', [])
        
        # Get available modules for the subject
        available_modules = self.module_library.get(subject, [])
        if not available_modules:
            return self._create_empty_path(user_profile.get('user_id', 'unknown'), subject)
        
        # Filter modules based on user's current level
        suitable_modules = self._filter_modules_by_level(available_modules, knowledge_level)
        
        # Sort modules by prerequisites and difficulty
        ordered_modules = self._order_modules_by_prerequisites(suitable_modules)
        
        # Adapt modules based on learning style
        adapted_modules = self._adapt_modules_for_learning_style(ordered_modules, learning_style)
        
        # Create progressive difficulty curve
        final_modules = self._create_difficulty_progression(adapted_modules, target_difficulty)
        
        # Calculate total time and create path
        total_time = sum(module.estimated_time for module in final_modules)
        difficulty_progression = [module.difficulty for module in final_modules]
        
        path = LearningPath(
            id=f"path_{user_profile.get('user_id', 'unknown')}_{subject.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}",
            title=f"Personalized {subject} Learning Path",
            description=f"Customized {subject} curriculum for {learning_style} learner",
            user_id=user_profile.get('user_id', 'unknown'),
            subject=subject,
            modules=final_modules,
            total_estimated_time=total_time,
            difficulty_progression=difficulty_progression,
            created_at=datetime.now(),
            last_updated=datetime.now()
        )
        
        return path
    
    def _filter_modules_by_level(self, modules: List[LearningModule], 
                                knowledge_level: int) -> List[LearningModule]:
        """Filter modules appropriate for user's knowledge level"""
        # Include modules at user's level and slightly above for challenge
        max_difficulty = min(knowledge_level + 2, 5)
        return [module for module in modules if module.difficulty <= max_difficulty]
    
    def _order_modules_by_prerequisites(self, modules: List[LearningModule]) -> List[LearningModule]:
        """Order modules based on prerequisites"""
        ordered = []
        remaining = modules.copy()
        
        while remaining:
            # Find modules with satisfied prerequisites
            ready_modules = []
            for module in remaining:
                if all(prereq in [m.id for m in ordered] for prereq in module.prerequisites):
                    ready_modules.append(module)
            
            if not ready_modules:
                # If no modules are ready, add modules without prerequisites
                ready_modules = [m for m in remaining if not m.prerequisites]
            
            if not ready_modules:
                # If still no modules, break to avoid infinite loop
                break
            
            # Sort ready modules by difficulty
            ready_modules.sort(key=lambda x: x.difficulty)
            
            # Add the first ready module
            if ready_modules:
                selected = ready_modules[0]
                ordered.append(selected)
                remaining.remove(selected)
        
        return ordered
    
    def _adapt_modules_for_learning_style(self, modules: List[LearningModule], 
                                        learning_style: str) -> List[LearningModule]:
        """Adapt module selection and order based on learning style"""
        adapted = []
        
        for module in modules:
            # Create a copy to avoid modifying the original
            adapted_module = LearningModule(
                id=module.id,
                title=module.title,
                description=module.description,
                subject=module.subject,
                difficulty=module.difficulty,
                prerequisites=module.prerequisites.copy(),
                estimated_time=module.estimated_time,
                content_type=module.content_type,
                topics=module.topics.copy(),
                learning_objectives=module.learning_objectives.copy()
            )
            
            # Adjust based on learning style
            if learning_style == "Visual":
                # Visual learners benefit from diagrams and examples
                if "examples" not in adapted_module.description:
                    adapted_module.description += " (includes visual examples and diagrams)"
                adapted_module.estimated_time = int(adapted_module.estimated_time * 0.9)  # Faster with visuals
                
            elif learning_style == "Auditory":
                # Auditory learners benefit from explanations and discussions
                adapted_module.description += " (includes audio explanations)"
                adapted_module.estimated_time = int(adapted_module.estimated_time * 1.1)  # More time for listening
                
            elif learning_style == "Kinesthetic":
                # Kinesthetic learners need hands-on practice
                if module.content_type == "lesson":
                    adapted_module.description += " (includes hands-on exercises)"
                    adapted_module.estimated_time = int(adapted_module.estimated_time * 1.2)  # More practice time
                
            elif learning_style == "Reading/Writing":
                # Reading/Writing learners prefer text-based content
                adapted_module.description += " (includes comprehensive notes and exercises)"
            
            adapted.append(adapted_module)
        
        return adapted
    
    def _create_difficulty_progression(self, modules: List[LearningModule], 
                                     target_difficulty: Optional[int] = None) -> List[LearningModule]:
        """Create a smooth difficulty progression"""
        if not modules:
            return modules
        
        # Sort by current difficulty
        modules.sort(key=lambda x: x.difficulty)
        
        # If target difficulty is specified, filter accordingly
        if target_difficulty:
            modules = [m for m in modules if m.difficulty <= target_difficulty]
        
        # Ensure we have a good mix of content types
        final_modules = []
        lesson_modules = [m for m in modules if m.content_type == "lesson"]
        quiz_modules = [m for m in modules if m.content_type == "quiz"]
        project_modules = [m for m in modules if m.content_type == "project"]
        
        # Interleave different types for better learning
        i = 0
        while i < len(lesson_modules):
            final_modules.append(lesson_modules[i])
            
            # Add quiz after every 2 lessons
            if (i + 1) % 2 == 0 and quiz_modules:
                quiz = next((q for q in quiz_modules if q.difficulty <= lesson_modules[i].difficulty + 1), None)
                if quiz and quiz not in final_modules:
                    final_modules.append(quiz)
            
            # Add project after every 3 lessons
            if (i + 1) % 3 == 0 and project_modules:
                project = next((p for p in project_modules if p.difficulty <= lesson_modules[i].difficulty + 1), None)
                if project and project not in final_modules:
                    final_modules.append(project)
            
            i += 1
        
        return final_modules
    
    def _create_empty_path(self, user_id: str, subject: str) -> LearningPath:
        """Create an empty learning path when no modules are available"""
        return LearningPath(
            id=f"empty_path_{user_id}_{subject.lower().replace(' ', '_')}",
            title=f"{subject} Learning Path",
            description=f"No modules available for {subject} at this time",
            user_id=user_id,
            subject=subject,
            modules=[],
            total_estimated_time=0,
            difficulty_progression=[],
            created_at=datetime.now(),
            last_updated=datetime.now()
        )
    
    def update_path_progress(self, path: LearningPath, completed_module_id: str, 
                           performance_score: float) -> LearningPath:
        """Update learning path based on user progress and performance"""
        
        # Find the completed module
        completed_module = next((m for m in path.modules if m.id == completed_module_id), None)
        if not completed_module:
            return path
        
        # Analyze performance and adjust future modules
        if performance_score < 0.7:  # Struggling
            # Add more practice modules or reduce difficulty
            self._add_remedial_content(path, completed_module)
        elif performance_score > 0.9:  # Excelling
            # Skip some basic content or add advanced modules
            self._add_advanced_content(path, completed_module)
        
        # Update path metadata
        path.last_updated = datetime.now()
        
        return path
    
    def _add_remedial_content(self, path: LearningPath, struggling_module: LearningModule):
        """Add additional practice content for struggling students"""
        # Find position of struggling module
        module_index = path.modules.index(struggling_module)
        
        # Create a practice module
        practice_module = LearningModule(
            id=f"practice_{struggling_module.id}",
            title=f"Extra Practice: {struggling_module.title}",
            description=f"Additional practice for {struggling_module.title}",
            subject=struggling_module.subject,
            difficulty=max(1, struggling_module.difficulty - 1),
            prerequisites=[struggling_module.id],
            estimated_time=30,
            content_type="practice",
            topics=struggling_module.topics,
            learning_objectives=[f"Reinforce {obj}" for obj in struggling_module.learning_objectives]
        )
        
        # Insert after the struggling module
        path.modules.insert(module_index + 1, practice_module)
    
    def _add_advanced_content(self, path: LearningPath, mastered_module: LearningModule):
        """Add advanced content for high-performing students"""
        # Find related advanced modules from the library
        available_modules = self.module_library.get(path.subject, [])
        advanced_modules = [
            m for m in available_modules 
            if m.difficulty > mastered_module.difficulty 
            and any(topic in mastered_module.topics for topic in m.topics)
            and m not in path.modules
        ]
        
        if advanced_modules:
            # Add the most relevant advanced module
            advanced_module = advanced_modules[0]
            path.modules.append(advanced_module)
    
    def get_next_module(self, path: LearningPath, completed_modules: List[str]) -> Optional[LearningModule]:
        """Get the next module in the learning path"""
        for module in path.modules:
            if module.id not in completed_modules:
                # Check if prerequisites are met
                if all(prereq in completed_modules for prereq in module.prerequisites):
                    return module
        return None
    
    def get_path_progress(self, path: LearningPath, completed_modules: List[str]) -> Dict[str, Any]:
        """Calculate progress statistics for a learning path"""
        total_modules = len(path.modules)
        completed_count = len([m for m in path.modules if m.id in completed_modules])
        
        completed_time = sum(
            module.estimated_time for module in path.modules 
            if module.id in completed_modules
        )
        
        progress_percentage = (completed_count / total_modules * 100) if total_modules > 0 else 0
        
        return {
            'total_modules': total_modules,
            'completed_modules': completed_count,
            'remaining_modules': total_modules - completed_count,
            'progress_percentage': progress_percentage,
            'estimated_time_completed': completed_time,
            'estimated_time_remaining': path.total_estimated_time - completed_time,
            'next_module': self.get_next_module(path, completed_modules)
        }