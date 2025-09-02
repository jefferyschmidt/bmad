export interface TechStackComponent {
  language?: string;
  framework?: string;
  library?: string;
  database?: string;
  platform?: string;
  containerization?: string;
}

export interface TechStack {
  id: string;
  name: string;
  description: string;
  frontend?: TechStackComponent;
  backend?: TechStackComponent;
  database?: TechStackComponent;
  deployment?: TechStackComponent;
}

export interface ApplicationType {
  id: string;
  name: string;
  description: string;
  techStacks: TechStack[];
}

export const APPLICATION_TYPES: ApplicationType[] = [
  {
    id: 'static_website',
    name: 'Static Website',
    description: 'A simple website with HTML, CSS, and JavaScript that can be hosted on any web server',
    techStacks: [
      {
        id: 'html_css_js',
        name: 'Pure HTML/CSS/JS',
        description: 'Traditional web development with HTML, CSS, and vanilla JavaScript',
        frontend: {
          language: 'HTML',
          framework: 'CSS',
          library: 'JavaScript'
        },
        deployment: {
          platform: 'Static Hosting',
          containerization: 'None'
        }
      },
      {
        id: 'jekyll',
        name: 'Jekyll',
        description: 'Static site generator perfect for blogs and documentation sites',
        frontend: {
          language: 'HTML',
          framework: 'Jekyll',
          library: 'Liquid'
        },
        deployment: {
          platform: 'GitHub Pages',
          containerization: 'None'
        }
      },
      {
        id: 'hugo',
        name: 'Hugo',
        description: 'Fast static site generator written in Go',
        frontend: {
          language: 'HTML',
          framework: 'Hugo',
          library: 'Go Templates'
        },
        deployment: {
          platform: 'Static Hosting',
          containerization: 'None'
        }
      }
    ]
  },
  {
    id: 'web_application',
    name: 'Web Application',
    description: 'A full-stack web application with frontend, backend, and database',
    techStacks: [
      {
        id: 'react_nodejs',
        name: 'React + Node.js',
        description: 'Modern JavaScript stack with React frontend and Node.js backend',
        frontend: {
          language: 'JavaScript',
          framework: 'React.js',
          library: 'Material-UI'
        },
        backend: {
          language: 'Node.js',
          framework: 'Express.js'
        },
        database: {
          database: 'PostgreSQL'
        },
        deployment: {
          platform: 'Cloud',
          containerization: 'Docker'
        }
      },
      {
        id: 'vue_python',
        name: 'Vue.js + Python',
        description: 'Vue.js frontend with Python FastAPI backend',
        frontend: {
          language: 'JavaScript',
          framework: 'Vue.js',
          library: 'Vuetify'
        },
        backend: {
          language: 'Python',
          framework: 'FastAPI'
        },
        database: {
          database: 'PostgreSQL'
        },
        deployment: {
          platform: 'Cloud',
          containerization: 'Docker'
        }
      },
      {
        id: 'nextjs_prisma',
        name: 'Next.js + Prisma',
        description: 'Full-stack React framework with modern database toolkit',
        frontend: {
          language: 'TypeScript',
          framework: 'Next.js',
          library: 'Tailwind CSS'
        },
        backend: {
          language: 'TypeScript',
          framework: 'Next.js API Routes'
        },
        database: {
          database: 'PostgreSQL'
        },
        deployment: {
          platform: 'Vercel',
          containerization: 'None'
        }
      }
    ]
  },
  {
    id: 'mobile_app',
    name: 'Mobile Application',
    description: 'A mobile application that can run on iOS and Android devices',
    techStacks: [
      {
        id: 'react_native',
        name: 'React Native',
        description: 'Cross-platform mobile development with React Native',
        frontend: {
          language: 'JavaScript',
          framework: 'React Native',
          library: 'Expo'
        },
        backend: {
          language: 'Node.js',
          framework: 'Express.js'
        },
        database: {
          database: 'PostgreSQL'
        },
        deployment: {
          platform: 'App Stores',
          containerization: 'None'
        }
      },
      {
        id: 'flutter_python',
        name: 'Flutter + Python',
        description: 'Flutter mobile app with Python backend',
        frontend: {
          language: 'Dart',
          framework: 'Flutter',
          library: 'Material Design'
        },
        backend: {
          language: 'Python',
          framework: 'FastAPI'
        },
        database: {
          database: 'PostgreSQL'
        },
        deployment: {
          platform: 'App Stores',
          containerization: 'None'
        }
      },
      {
        id: 'ionic_nodejs',
        name: 'Ionic + Node.js',
        description: 'Hybrid mobile app with Ionic and Node.js backend',
        frontend: {
          language: 'TypeScript',
          framework: 'Ionic',
          library: 'Angular'
        },
        backend: {
          language: 'Node.js',
          framework: 'Express.js'
        },
        database: {
          database: 'PostgreSQL'
        },
        deployment: {
          platform: 'App Stores',
          containerization: 'None'
        }
      }
    ]
  },
  {
    id: 'automation_script',
    name: 'Automation Script',
    description: 'A script or tool to automate tasks and workflows',
    techStacks: [
      {
        id: 'python_script',
        name: 'Python Script',
        description: 'Python automation script with libraries for various tasks',
        backend: {
          language: 'Python',
          framework: 'Standard Library'
        },
        deployment: {
          platform: 'Local/Server',
          containerization: 'None'
        }
      },
      {
        id: 'nodejs_script',
        name: 'Node.js Script',
        description: 'JavaScript automation script using Node.js',
        backend: {
          language: 'Node.js',
          framework: 'Standard Library'
        },
        deployment: {
          platform: 'Local/Server',
          containerization: 'None'
        }
      },
      {
        id: 'powershell_script',
        name: 'PowerShell Script',
        description: 'PowerShell automation script for Windows environments',
        backend: {
          language: 'PowerShell',
          framework: 'PowerShell Core'
        },
        deployment: {
          platform: 'Windows',
          containerization: 'None'
        }
      },
      {
        id: 'bash_script',
        name: 'Bash Script',
        description: 'Bash shell script for Unix/Linux automation',
        backend: {
          language: 'Bash',
          framework: 'Shell'
        },
        deployment: {
          platform: 'Unix/Linux',
          containerization: 'None'
        }
      }
    ]
  },
  {
    id: 'desktop_app',
    name: 'Desktop Application',
    description: 'A desktop application that runs on Windows, macOS, or Linux',
    techStacks: [
      {
        id: 'electron_react',
        name: 'Electron + React',
        description: 'Cross-platform desktop app using Electron and React',
        frontend: {
          language: 'JavaScript',
          framework: 'React.js',
          library: 'Electron'
        },
        backend: {
          language: 'Node.js',
          framework: 'Electron'
        },
        deployment: {
          platform: 'Desktop',
          containerization: 'None'
        }
      },
      {
        id: 'python_tkinter',
        name: 'Python Tkinter',
        description: 'Desktop app using Python with Tkinter GUI framework',
        frontend: {
          language: 'Python',
          framework: 'Tkinter',
          library: 'Standard Library'
        },
        backend: {
          language: 'Python',
          framework: 'Standard Library'
        },
        deployment: {
          platform: 'Desktop',
          containerization: 'None'
        }
      },
      {
        id: 'nodejs_electron',
        name: 'Node.js + Electron',
        description: 'Desktop app using Node.js with Electron framework',
        frontend: {
          language: 'JavaScript',
          framework: 'Electron',
          library: 'HTML/CSS'
        },
        backend: {
          language: 'Node.js',
          framework: 'Electron'
        },
        deployment: {
          platform: 'Desktop',
          containerization: 'None'
        }
      }
    ]
  }
];

export const getApplicationTypeById = (id: string): ApplicationType | undefined => {
  return APPLICATION_TYPES.find(type => type.id === id);
};

export const getTechStackById = (applicationTypeId: string, techStackId: string): TechStack | undefined => {
  const applicationType = getApplicationTypeById(applicationTypeId);
  return applicationType?.techStacks.find(stack => stack.id === techStackId);
};
