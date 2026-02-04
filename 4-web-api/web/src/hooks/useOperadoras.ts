// src/hooks/useOperadoras.ts
import { useQuery } from "@tanstack/react-query";
import axios from "axios"; 
import { Operadora, PaginatedResponse, Estatisticas, Despesa } from "@/types";

const api = axios.create({
  baseURL: "http://localhost:8000/api",
});

export function useOperadoras(page: number, busca: string) {
  return useQuery({
    queryKey: ["operadoras", page, busca],
    queryFn: async () => {
      console.log("BUSCANDO DADOS VIA AXIOS DIRETO...");

      const params = { page, limit: 10, busca: busca || undefined };

      const { data } = await api.get<PaginatedResponse<Operadora>>(
        "/operadoras",
        { params },
      );
      return data;
    },
    placeholderData: (previousData) => previousData,
  });
}

export function useEstatisticas() {
  return useQuery({
    queryKey: ["estatisticas"],
    queryFn: async () => {
      const { data } = await api.get<Estatisticas>("/estatisticas");
      return data;
    },
  });
}

export function useOperadoraDetalhes(cnpj: string) {
  return useQuery({
    queryKey: ["operadora", cnpj],
    queryFn: async () => {
      const [opRes, despRes] = await Promise.all([
        api.get<Operadora>(`/operadoras/${cnpj}`),
        api.get<Despesa[]>(`/operadoras/${cnpj}/despesas`),
      ]);
      return {
        operadora: opRes.data,
        despesas: despRes.data,
      };
    },
    enabled: !!cnpj,
  });
}
