"use client";

import React from "react";
import { useParams, useRouter } from "next/navigation";
import { useOperadoraDetalhes } from "@/hooks/useOperadoras";

export default function DetalhesOperadora() {
  const params = useParams();
  const router = useRouter();
  const cnpj = params.cnpj as string;

  const { data, isLoading, isError } = useOperadoraDetalhes(cnpj);

  if (isLoading)
    return (
      <div className="flex h-screen items-center justify-center text-gray-500">
        Carregando detalhes...
      </div>
    );
  if (isError || !data)
    return (
      <div className="flex h-screen items-center justify-center text-red-500">
        Erro ao carregar operadora ou não encontrada.
      </div>
    );

  const { operadora, despesas } = data;

  return (
    <main className="max-w-4xl mx-auto p-6">
      <button
        onClick={() => router.back()}
        className="mb-6 text-gray-500 hover:text-blue-600 flex items-center gap-2 transition font-medium"
      >
        ← Voltar para Dashboard
      </button>

      <div className="bg-white p-8 rounded-xl shadow-sm border border-gray-200 mb-8">
        <h1 className="text-2xl font-bold text-gray-800 mb-6">
          {operadora.RAZAO_SOCIAL}
        </h1>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-sm">
          <div>
            <span className="block text-gray-400 mb-1">CNPJ</span>
            <span className="font-medium text-gray-900 text-lg">
              {operadora.CNPJ}
            </span>
          </div>
          <div>
            <span className="block text-gray-400 mb-1">Registro ANS</span>
            <span className="font-medium text-gray-900 text-lg">
              {operadora.REG_ANS}
            </span>
          </div>
          <div>
            <span className="block text-gray-400 mb-1">UF</span>
            <span className="font-medium text-gray-900 text-lg">
              {operadora.UF}
            </span>
          </div>
          <div>
            <span className="block text-gray-400 mb-1">Modalidade</span>
            <span className="font-medium text-gray-900 text-lg">
              {operadora.MODALIDADE}
            </span>
          </div>
        </div>
      </div>

      <h3 className="text-xl font-semibold text-gray-500 mb-4 border-l-4 border-blue-500 pl-3">
        Histórico Financeiro
      </h3>

      <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
        {despesas.length === 0 ? (
          <div className="p-8 text-center text-gray-500">
            Nenhum registro de despesa encontrado para esta operadora.
          </div>
        ) : (
          <table className="w-full text-left">
            <thead className="bg-gray-50 border-b border-gray-200">
              <tr>
                <th className="p-4 text-sm font-semibold text-gray-600">
                  Data
                </th>
                <th className="p-4 text-sm font-semibold text-gray-600">
                  Descrição
                </th>
                <th className="p-4 text-sm font-semibold text-gray-600 text-right">
                  Valor
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {despesas.map((d, idx) => (
                <tr key={idx} className="hover:bg-gray-50 transition-colors">
                  <td className="p-4 text-sm text-gray-600 w-32">
                    {d.DATA_EVENTO}
                  </td>
                  <td className="p-4 text-sm text-gray-800">{d.DESCRICAO}</td>
                  <td className="p-4 text-sm font-medium text-red-600 text-right w-40 whitespace-nowrap">
                    {Number(d.VALOR).toLocaleString("pt-BR", {
                      style: "currency",
                      currency: "BRL",
                    })}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </main>
  );
}
