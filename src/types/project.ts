export interface Project {
  id: number;
  name: string;
  description?: string;
  requirements: string;
  refined_requirements?: string;
  data_model?: string;
  system_architecture?: string;
  status: string;
  archived: boolean;
  ai_provider: string;
  created_at: string;
  updated_at: string;
}

export interface AIProvider {
  id: number;
  name: string;
  display_name: string;
  model_name: string;
  max_tokens: number;
  is_active: boolean;
  created_at: string;
}

export type PipelineStage = 'requirements' | 'data-model' | 'architecture';

export interface StageConfig {
  key: PipelineStage;
  label: string;
  icon: React.ReactNode;
  available: boolean;
  completed: boolean;
}
