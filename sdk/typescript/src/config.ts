export interface AIHedgeFundConfig {
  apiKey?: string;
  baseUrl?: string;
  timeout?: number;
}

export const DEFAULT_CONFIG: AIHedgeFundConfig = {
  baseUrl: 'http://localhost:8000',
  timeout: 30000,
};