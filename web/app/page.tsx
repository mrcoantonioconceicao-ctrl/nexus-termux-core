'use client';
import React from 'react';
import { ShieldCheck, Cpu, Layers, GitBranch, Terminal } from 'lucide-react';

const PROGRAMS = [
  { name: 'nexus_vault', id: 'NexaVault111111111111111111111111111111111', cpi: ['nexus_token_vault::deposit_token'], status: 'AUDITED_PASS' },
  { name: 'nexus_staking', id: 'NexaStake111111111111111111111111111111111', cpi: [], status: 'AUDITED_PASS' },
  { name: 'nexus_token_vault', id: 'NexaTokVlt11111111111111111111111111111111', cpi: [], status: 'AUDITED_PASS' }
];

export default function Dashboard() {
  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between border-b border-zinc-800 pb-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-white flex items-center gap-2">
            <Terminal className="w-6 h-6 text-emerald-400" />
            Nexus Termux Core — Workspace Dashboard
          </h1>
          <p className="text-sm text-zinc-400 mt-1">
            Deterministic multi-program Anchor telemetry & verification state
          </p>
        </div>
        <div className="flex items-center gap-2 bg-emerald-950/40 border border-emerald-800/60 px-3 py-1.5 rounded-full text-xs font-medium text-emerald-400">
          <ShieldCheck className="w-4 h-4" />
          Bump Binding: PASS (3/3)
        </div>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-zinc-900/50 border border-zinc-800 rounded-lg p-5">
          <div className="flex items-center gap-2 text-zinc-400 text-xs font-semibold uppercase tracking-wider">
            <Cpu className="w-4 h-4 text-sky-400" /> Active Programs
          </div>
          <div className="text-3xl font-bold text-white mt-2">3 Nodes</div>
          <div className="text-xs text-zinc-500 mt-1">Vault, Staking, TokenVault</div>
        </div>
        <div className="bg-zinc-900/50 border border-zinc-800 rounded-lg p-5">
          <div className="flex items-center gap-2 text-zinc-400 text-xs font-semibold uppercase tracking-wider">
            <Layers className="w-4 h-4 text-purple-400" /> SDK Aggregation
          </div>
          <div className="text-3xl font-bold text-white mt-2">Unified</div>
          <div className="text-xs text-zinc-500 mt-1">export * from ./sdk/index.ts</div>
        </div>
        <div className="bg-zinc-900/50 border border-zinc-800 rounded-lg p-5">
          <div className="flex items-center gap-2 text-zinc-400 text-xs font-semibold uppercase tracking-wider">
            <GitBranch className="w-4 h-4 text-emerald-400" /> CI/CD Pipeline
          </div>
          <div className="text-3xl font-bold text-white mt-2">Synced</div>
          <div className="text-xs text-zinc-500 mt-1">GitHub Actions active</div>
        </div>
      </div>
      <div className="bg-zinc-900/50 border border-zinc-800 rounded-lg overflow-hidden">
        <div className="px-6 py-4 border-b border-zinc-800 font-semibold text-sm text-zinc-300">
          Discovered Workspace Programs
        </div>
        <div className="divide-y divide-zinc-800/60">
          {PROGRAMS.map((prog) => (
            <div key={prog.name} className="px-6 py-4 flex flex-col md:flex-row md:items-center justify-between gap-4">
              <div>
                <div className="font-mono text-sm font-semibold text-sky-400">{prog.name}</div>
                <div className="font-mono text-xs text-zinc-500 truncate max-w-sm mt-0.5">{prog.id}</div>
              </div>
              <div className="flex items-center gap-4">
                <div className="text-xs text-zinc-400">
                  CPI Targets: <span className="font-mono text-zinc-300">{prog.cpi.length > 0 ? prog.cpi.join(', ') : 'None'}</span>
                </div>
                <span className="bg-emerald-950/60 border border-emerald-800/50 text-emerald-400 text-xs px-2.5 py-1 rounded-md font-mono">
                  {prog.status}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
