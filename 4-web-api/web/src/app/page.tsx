"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import { useOperadoras, useEstatisticas } from "@/hooks/useOperadoras";
import {Ubuntu} from "next/font/google"

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
);

const ubuntu = Ubuntu({
  weight: ["300", "400", "500", "700"],
  subsets: ["latin"]
})

export default function Dashboard() {
  const router = useRouter();
  const [page, setPage] = useState(1);
  const [busca, setBusca] = useState("");

  const { data: statsData, isLoading: isLoadingStats } = useEstatisticas();
  const {
    data: opsData,
    isLoading: isLoadingOps,
    isFetching,
  } = useOperadoras(page, busca);

  const chartConfig = {
    labels:
      statsData?.top_5_operadoras.map(
        (op) => op.RAZAO_SOCIAL.substring(0, 15) + "...",
      ) || [],
    datasets: [
      {
        label: "Total de Despesas (R$)",
        data:
          statsData?.top_5_operadoras.map((op) => op.TOTAL_DESPESAS || 0) || [],
        backgroundColor: "rgba(59, 130, 246, 0.6)",
      },
    ],
  };

  return (
    <main className="max-w-6xl mx-auto p-6">
      <h1
        className={`text-3xl font-bold text-gray-400 mb-8 border-b pb-4 text-center font-sans ${ubuntu.className}`}
      >
        Dashboard Intuitive Care
      </h1>

      <section className="bg-white p-6 rounded-xl shadow-sm border border-gray-200 mb-8">
        <h2
          className={`text-xl font-semibold mb-6 text-gray-700 ${ubuntu.className}`}
        >
          Top 5 Maiores Despesas
        </h2>
        <div className="h-64 flex items-center justify-center">
          {isLoadingStats ? (
            <div className="text-gray-400 animate-pulse">
              Carregando estatísticas...
            </div>
          ) : (
            <Bar
              data={chartConfig}
              options={{ maintainAspectRatio: false, responsive: true }}
            />
          )}
        </div>
      </section>

      <section className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
        <div className="flex flex-col md:flex-row justify-between items-center mb-6 gap-4">
          <h2 className={`text-xl font-semibold text-gray-700 ${ubuntu.className}`}>
            Operadoras Cadastradas
          </h2>
          <input
            type="text"
            placeholder="Buscar por Razão Social ou CNPJ..."
            className="border border-gray-300 text-gray-600 rounded-lg px-4 py-2 w-full md:w-80 focus:ring-2 focus:ring-blue-500 outline-none transition"
            value={busca}
            onChange={(e) => {
              setBusca(e.target.value);
              setPage(1);
            }}
          />
        </div>

        <div className="overflow-x-auto">
          {isLoadingOps ? (
            <div className="p-10 text-center text-gray-500">
              Carregando operadoras...
            </div>
          ) : (
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-gray-50 text-gray-600 text-sm uppercase tracking-wider">
                  <th className="p-4 border-b">Reg. ANS</th>
                  <th className="p-4 border-b">CNPJ</th>
                  <th className="p-4 border-b">Razão Social</th>
                  <th className="p-4 border-b text-center">Ações</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {opsData?.data.map((op) => (
                  <tr
                    key={op.REG_ANS}
                    className="hover:bg-blue-50 transition-colors"
                  >
                    <td className="p-4 text-gray-600">{op.REG_ANS}</td>
                    <td className="p-4 text-gray-600">{op.CNPJ}</td>
                    <td className="p-4 font-medium text-gray-800">
                      {op.RAZAO_SOCIAL}
                    </td>
                    <td className="p-4 text-center">
                      <button
                        onClick={() => router.push(`/operadora/${op.CNPJ}`)}
                        className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 text-sm font-medium transition shadow-sm"
                      >
                        Detalhes
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>

        <div className="flex justify-between items-center mt-6 pt-4 border-t border-gray-100">
          <button
            disabled={page === 1}
            onClick={() => setPage((p) => p - 1)}
            className="px-4 py-2 border rounded-md text-gray-600 disabled:opacity-50 hover:bg-gray-50 transition"
          >
            Anterior
          </button>

          <span className="text-sm text-gray-500">
            Página <span className="font-bold text-gray-800">{page}</span> de{" "}
            {opsData?.total_pages || 1}
            {isFetching && (
              <span className="ml-2 text-blue-500 text-xs font-semibold">
                (Atualizando...)
              </span>
            )}
          </span>

          <button
            disabled={page === (opsData?.total_pages || 1)}
            onClick={() => setPage((p) => p + 1)}
            className="px-4 py-2 border rounded-md text-gray-600 disabled:opacity-50 hover:bg-gray-50 transition"
          >
            Próxima
          </button>
        </div>
      </section>
    </main>
  );
}
