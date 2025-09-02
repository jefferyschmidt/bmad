"""
Application types and tech stacks constants for AI agents
"""

from typing import Dict, List, Any

APPLICATION_TYPES = {
    "static_website": {
        "name": "Static Website",
        "description": "A simple website with static content, ideal for blogs, portfolios, or informational sites.",
        "tech_stacks": [
            {
                "id": "html_css_js",
                "name": "Pure HTML/CSS/JS",
                "description": "Basic static site with no frameworks.",
                "frontend": {"name": "HTML/CSS/JS", "language": "HTML", "framework": "None", "styling": "CSS"},
                "backend": {"name": "None", "language": "None", "framework": "None"},
                "database": {"name": "None", "type": "None"},
                "deployment": {"name": "Static Hosting", "platform": "Static Hosting", "containerization": "None"}
            },
            {
                "id": "jekyll",
                "name": "Jekyll",
                "description": "Static site generator perfect for blogs and documentation sites.",
                "frontend": {"name": "Jekyll", "language": "Ruby", "framework": "Jekyll", "styling": "Liquid"},
                "backend": {"name": "None", "language": "None", "framework": "None"},
                "database": {"name": "None", "type": "None"},
                "deployment": {"name": "GitHub Pages", "platform": "GitHub Pages", "containerization": "None"}
            },
            {
                "id": "hugo",
                "name": "Hugo",
                "description": "Fast static site generator written in Go.",
                "frontend": {"name": "Hugo", "language": "Go", "framework": "Hugo", "styling": "Go Templates"},
                "backend": {"name": "None", "language": "None", "framework": "None"},
                "database": {"name": "None", "type": "None"},
                "deployment": {"name": "Static Hosting", "platform": "Static Hosting", "containerization": "None"}
            }
        ]
    },
    "web_application": {
        "name": "Web Application",
        "description": "A dynamic web application with backend functionality, user authentication, and database integration.",
        "tech_stacks": [
            {
                "id": "react_nodejs",
                "name": "React + Node.js",
                "description": "Modern full-stack JavaScript application.",
                "frontend": {"name": "React", "language": "JavaScript", "framework": "React", "styling": "CSS/SCSS"},
                "backend": {"name": "Node.js", "language": "JavaScript", "framework": "Express.js"},
                "database": {"name": "PostgreSQL", "type": "Relational"},
                "deployment": {"name": "Cloud", "platform": "Cloud", "containerization": "Docker"}
            },
            {
                "id": "vue_python",
                "name": "Vue.js + Python",
                "description": "Vue.js frontend with Python backend using FastAPI.",
                "frontend": {"name": "Vue.js", "language": "JavaScript", "framework": "Vue.js", "styling": "CSS/SCSS"},
                "backend": {"name": "Python", "language": "Python", "framework": "FastAPI"},
                "database": {"name": "PostgreSQL", "type": "Relational"},
                "deployment": {"name": "Cloud", "platform": "Cloud", "containerization": "Docker"}
            },
            {
                "id": "nextjs_prisma",
                "name": "Next.js + Prisma",
                "description": "Full-stack React framework with modern database toolkit.",
                "frontend": {"name": "Next.js", "language": "TypeScript", "framework": "Next.js", "styling": "Tailwind CSS"},
                "backend": {"name": "Next.js API", "language": "TypeScript", "framework": "Next.js"},
                "database": {"name": "PostgreSQL", "type": "Relational"},
                "deployment": {"name": "Vercel", "platform": "Vercel", "containerization": "None"}
            }
        ]
    },
    "mobile_app": {
        "name": "Mobile App",
        "description": "A mobile application for iOS and/or Android platforms.",
        "tech_stacks": [
            {
                "id": "react_native",
                "name": "React Native",
                "description": "Cross-platform mobile development with JavaScript.",
                "frontend": {"name": "React Native", "language": "JavaScript", "framework": "React Native", "styling": "StyleSheet"},
                "backend": {"name": "Node.js", "language": "JavaScript", "framework": "Express.js"},
                "database": {"name": "PostgreSQL", "type": "Relational"},
                "deployment": {"name": "App Stores", "platform": "App Stores", "containerization": "None"}
            },
            {
                "id": "flutter_python",
                "name": "Flutter + Python",
                "description": "Cross-platform mobile with Flutter and Python backend.",
                "frontend": {"name": "Flutter", "language": "Dart", "framework": "Flutter", "styling": "Material Design"},
                "backend": {"name": "Python", "language": "Python", "framework": "FastAPI"},
                "database": {"name": "PostgreSQL", "type": "Relational"},
                "deployment": {"name": "App Stores", "platform": "App Stores", "containerization": "None"}
            },
            {
                "id": "ionic_nodejs",
                "name": "Ionic + Node.js",
                "description": "Hybrid mobile app with web technologies.",
                "frontend": {"name": "Ionic", "language": "TypeScript", "framework": "Ionic", "styling": "CSS/SCSS"},
                "backend": {"name": "Node.js", "language": "JavaScript", "framework": "Express.js"},
                "database": {"name": "PostgreSQL", "type": "Relational"},
                "deployment": {"name": "App Stores", "platform": "App Stores", "containerization": "None"}
            }
        ]
    },
    "automation_script": {
        "name": "Automation/Script",
        "description": "A script or automation tool for system administration, data processing, or workflow automation.",
        "tech_stacks": [
            {
                "id": "python_script",
                "name": "Python Script",
                "description": "Python automation script for various tasks.",
                "frontend": {"name": "None", "language": "None", "framework": "None", "styling": "None"},
                "backend": {"name": "Python", "language": "Python", "framework": "None"},
                "database": {"name": "SQLite", "type": "Relational"},
                "deployment": {"name": "Local/Server", "platform": "Local/Server", "containerization": "None"}
            },
            {
                "id": "nodejs_script",
                "name": "Node.js Script",
                "description": "JavaScript automation script using Node.js.",
                "frontend": {"name": "None", "language": "None", "framework": "None", "styling": "None"},
                "backend": {"name": "Node.js", "language": "JavaScript", "framework": "None"},
                "database": {"name": "SQLite", "type": "Relational"},
                "deployment": {"name": "Local/Server", "platform": "Local/Server", "containerization": "None"}
            },
            {
                "id": "powershell_script",
                "name": "PowerShell Script",
                "description": "Windows PowerShell automation script.",
                "frontend": {"name": "None", "language": "None", "framework": "None", "styling": "None"},
                "backend": {"name": "PowerShell", "language": "PowerShell", "framework": "None"},
                "database": {"name": "None", "type": "None"},
                "deployment": {"name": "Windows", "platform": "Windows", "containerization": "None"}
            },
            {
                "id": "bash_script",
                "name": "Bash Script",
                "description": "Unix/Linux shell automation script.",
                "frontend": {"name": "None", "language": "None", "framework": "None", "styling": "None"},
                "backend": {"name": "Bash", "language": "Bash", "framework": "None"},
                "database": {"name": "None", "type": "None"},
                "deployment": {"name": "Unix/Linux", "platform": "Unix/Linux", "containerization": "None"}
            }
        ]
    },
    "desktop_application": {
        "name": "Desktop Application",
        "description": "A desktop application for Windows, macOS, or Linux.",
        "tech_stacks": [
            {
                "id": "electron_react",
                "name": "Electron + React",
                "description": "Cross-platform desktop app with web technologies.",
                "frontend": {"name": "React", "language": "JavaScript", "framework": "React", "styling": "CSS/SCSS"},
                "backend": {"name": "Electron", "language": "JavaScript", "framework": "Electron"},
                "database": {"name": "SQLite", "type": "Relational"},
                "deployment": {"name": "Desktop", "platform": "Desktop", "containerization": "None"}
            },
            {
                "id": "python_tkinter",
                "name": "Python Tkinter",
                "description": "Python desktop application with Tkinter GUI.",
                "frontend": {"name": "Tkinter", "language": "Python", "framework": "Tkinter", "styling": "Tkinter"},
                "backend": {"name": "Python", "language": "Python", "framework": "None"},
                "database": {"name": "SQLite", "type": "Relational"},
                "deployment": {"name": "Desktop", "platform": "Desktop", "containerization": "None"}
            },
            {
                "id": "nodejs_electron",
                "name": "Node.js + Electron",
                "description": "Desktop application using Node.js and Electron.",
                "frontend": {"name": "HTML/CSS/JS", "language": "JavaScript", "framework": "Electron", "styling": "CSS"},
                "backend": {"name": "Node.js", "language": "JavaScript", "framework": "Electron"},
                "database": {"name": "SQLite", "type": "Relational"},
                "deployment": {"name": "Desktop", "platform": "Desktop", "containerization": "None"}
            }
        ]
    }
}

def get_tech_stacks_for_application_type(application_type: str) -> List[Dict[str, Any]]:
    """Get available tech stacks for a given application type."""
    if application_type in APPLICATION_TYPES:
        return APPLICATION_TYPES[application_type]["tech_stacks"]
    return []

def get_tech_stack_by_id(application_type: str, tech_stack_id: str) -> Dict[str, Any]:
    """Get a specific tech stack by ID for a given application type."""
    tech_stacks = get_tech_stacks_for_application_type(application_type)
    for stack in tech_stacks:
        if stack["id"] == tech_stack_id:
            return stack
    return {}
