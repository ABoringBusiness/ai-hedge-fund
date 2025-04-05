import axios, { AxiosInstance } from 'axios';
import { AIHedgeFundConfig, DEFAULT_CONFIG } from './config';
import { HedgeFundResponse, Portfolio, RunOptions } from './models';

export class AIHedgeFundClient {
  private client: AxiosInstance;
  private config: AIHedgeFundConfig;

  constructor(config: AIHedgeFundConfig = {}) {
    this.config = { ...DEFAULT_CONFIG, ...config };
    
    this.client = axios.create({
      baseURL: this.config.baseUrl,
      timeout: this.config.timeout,
      headers: {
        'Content-Type': 'application/json',
        ...(this.config.apiKey ? { 'Authorization': `Bearer ${this.config.apiKey}` } : {}),
      },
    });
  }

  /**
   * Run the hedge fund with the specified options
   */
  async run(options: RunOptions): Promise<HedgeFundResponse> {
    try {
      const response = await this.client.post<HedgeFundResponse>('/run', {
        tickers: options.tickers,
        start_date: options.startDate,
        end_date: options.endDate,
        initial_cash: options.initialCash || 100000,
        margin_requirement: options.marginRequirement || 0,
        show_reasoning: options.showReasoning || false,
        selected_analysts: options.selectedAnalysts || [],
        model_name: options.modelName || 'gpt-4o',
        model_provider: options.modelProvider || 'OpenAI',
      });
      
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        throw new Error(`API request failed: ${error.message}`);
      }
      throw error;
    }
  }

  /**
   * Get available analysts
   */
  async getAnalysts(): Promise<string[]> {
    try {
      const response = await this.client.get<string[]>('/analysts');
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        throw new Error(`API request failed: ${error.message}`);
      }
      throw error;
    }
  }

  /**
   * Get available LLM models
   */
  async getModels(): Promise<string[]> {
    try {
      const response = await this.client.get<string[]>('/models');
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        throw new Error(`API request failed: ${error.message}`);
      }
      throw error;
    }
  }
}