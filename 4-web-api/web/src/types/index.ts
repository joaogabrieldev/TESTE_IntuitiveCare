export interface Operadora {
  REG_ANS: string;
  CNPJ: string;
  RAZAO_SOCIAL: string;
  UF: string;
  MODALIDADE: string;
  TOTAL_DESPESAS?: number;
}

export interface Despesa {
  DESCRICAO: string;
  DATA_EVENTO: string;
  VALOR: number;
}

export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  limit: number;
  total_pages: number;
}

export interface Estatisticas {
  total_geral_despesas: number;
  media_por_operadora: number;
  top_5_operadoras: Operadora[];
}
