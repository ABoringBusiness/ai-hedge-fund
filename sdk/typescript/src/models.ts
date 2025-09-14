export interface Portfolio {
  cash: number;
  margin_requirement: number;
  margin_used: number;
  positions: Record<string, Position>;
  realized_gains: Record<string, RealizedGains>;
}

export interface Position {
  long: number;
  short: number;
  long_cost_basis: number;
  short_cost_basis: number;
  short_margin_used: number;
}

export interface RealizedGains {
  long: number;
  short: number;
}

export interface TradeDecision {
  ticker: string;
  action: 'BUY' | 'SELL' | 'SHORT' | 'COVER' | 'HOLD';
  quantity: number;
  reasoning: string;
}

export interface AnalystSignal {
  ticker: string;
  signal: 'STRONG_BUY' | 'BUY' | 'HOLD' | 'SELL' | 'STRONG_SELL';
  confidence: number;
  reasoning: string;
}

export interface HedgeFundResponse {
  decisions: TradeDecision[];
  analyst_signals: Record<string, AnalystSignal[]>;
}

export interface RunOptions {
  tickers: string[];
  startDate?: string;
  endDate?: string;
  initialCash?: number;
  marginRequirement?: number;
  showReasoning?: boolean;
  selectedAnalysts?: string[];
  modelName?: string;
  modelProvider?: string;
}