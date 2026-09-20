import React, { useState } from 'react';
import { useFarm } from '../context/FarmContext';
import { useLanguage } from '../context/LanguageContext';
import VoiceSpeaker from '../components/common/VoiceSpeaker';
import {
  Bot,
  Brain,
  Layers,
  CloudSun,
  Sprout,
  Bug,
  TrendingUp,
  CalendarCheck,
  Cpu,
  Terminal,
  Activity,
  ArrowDown
} from 'lucide-react';

export default function AgentCenterPage() {
  const { agents, activityLogs } = useFarm();
  const { t, language } = useLanguage();
  const [selectedAgent, setSelectedAgent] = useState(agents[0]);

  const getAgentIcon = (id) => {
    switch (id) {
      case 'orchestrator': return <Brain className="w-5 h-5 text-emerald-400" />;
      case 'soil': return <Layers className="w-5 h-5 text-amber-400" />;
      case 'weather': return <CloudSun className="w-5 h-5 text-sky-400" />;
      case 'crop': return <Sprout className="w-5 h-5 text-green-400" />;
      case 'pest': return <Bug className="w-5 h-5 text-rose-400" />;
      case 'market': return <TrendingUp className="w-5 h-5 text-purple-400" />;
      case 'planner': return <CalendarCheck className="w-5 h-5 text-teal-400" />;
      case 'execution': return <Cpu className="w-5 h-5 text-blue-400" />;
      default: return <Bot className="w-5 h-5 text-emerald-400" />;
    }
  };

  return (
    <div className="space-y-6">
      
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-gradient-to-r from-slate-900 via-purple-950 to-slate-900 p-6 rounded-3xl text-white shadow-xl">
        <div>
          <div className="flex items-center gap-2">
            <span className="p-2 rounded-xl bg-purple-500/20 text-purple-300 border border-purple-400/30">
              <Bot className="w-5 h-5" />
            </span>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="text-xl sm:text-2xl font-extrabold tracking-tight">
                  {t("agentsPage.title", "AI Multi-Agent Control Center")}
                </h1>
                <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-purple-500/30 text-purple-200 border border-purple-400/40">
                  {t("agentsPage.specializedCount", "8 Specialized Agents")}
                </span>
              </div>
              <p className="text-xs text-purple-200/80">
                {t("agentsPage.subtitle", "Autonomous cooperative network coordinating soil telemetry, meteorology, vision disease detection & APMC markets")}
              </p>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <VoiceSpeaker
            text={language === 'gu'
              ? "ઓટોનોમસ મલ્ટી-એજન્ટ કંટ્રોલ સેન્ટર. ૮ વિશેષ AI એજન્ટો મળીને તમારા ખેતરનું સંકલન કરે છે."
              : "Autonomous multi-agent control center. Eight specialized agents collaborate continuously under the master orchestrator to monitor your farm."}
            label={t("agentsPage.explainArch", "Explain Architecture")}
            className="!bg-purple-900/50 !text-purple-200 !border-purple-700"
          />
        </div>
      </div>

      {/* Visual Multi-Agent Architecture Topology Diagram */}
      <div className="bg-slate-950 p-6 rounded-3xl border border-slate-800 shadow-2xl text-white space-y-6">
        <div className="flex items-center justify-between border-b border-slate-800 pb-3">
          <span className="text-xs font-bold text-slate-400 uppercase tracking-wider flex items-center gap-2">
            <Activity className="w-4 h-4 text-emerald-400 animate-pulse" />
            {t("agentsPage.topologyTitle", "Live Distributed Multi-Agent Topology")}
          </span>
          <span className="text-[11px] text-emerald-400 font-mono bg-emerald-950/80 px-2.5 py-1 rounded-full border border-emerald-800">
            {t("agentsPage.consensus", "SYSTEM CONSENSUS: 96%")}
          </span>
        </div>

        {/* Level 1: Master Orchestrator */}
        <div className="flex justify-center">
          <div
            onClick={() => setSelectedAgent(agents[0])}
            className={`cursor-pointer p-4 rounded-2xl border-2 transition-all w-80 text-center ${
              selectedAgent.id === 'orchestrator'
                ? 'border-emerald-400 bg-emerald-950/40 ring-4 ring-emerald-500/20 shadow-glow-green'
                : 'border-slate-700 bg-slate-900/90 hover:border-slate-500'
            }`}
          >
            <div className="flex items-center justify-center gap-2 text-emerald-400 font-extrabold text-sm">
              <Brain className="w-5 h-5" />
              <span>{t("agentsPage.masterOrchestrator", "MASTER ORCHESTRATOR AGENT")}</span>
            </div>
            <p className="text-[11px] text-slate-300 mt-1">{t("agentsPage.orchestratorDesc", "Coordinating & Synthesizing Multi-Domain Telemetry")}</p>
            <span className="inline-block mt-2 px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
              Confidence 96% • {t("common.active", "Active")}
            </span>
          </div>
        </div>

        {/* Connector Lines */}
        <div className="flex justify-center -my-2">
          <ArrowDown className="w-6 h-6 text-slate-600 animate-bounce" />
        </div>

        {/* Level 2: Specialized Sub-Agents */}
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3">
          {agents.slice(1, 6).map((ag) => {
            const isSelected = selectedAgent.id === ag.id;
            return (
              <div
                key={ag.id}
                onClick={() => setSelectedAgent(ag)}
                className={`p-3.5 rounded-2xl border-2 cursor-pointer transition-all ${
                  isSelected
                    ? 'border-purple-400 bg-purple-950/40 ring-4 ring-purple-500/20'
                    : 'border-slate-800 bg-slate-900/70 hover:border-slate-700'
                }`}
              >
                <div className="flex items-center gap-2">
                  {getAgentIcon(ag.id)}
                  <span className="font-bold text-xs text-white truncate">{ag.name.replace('Agent', '')}</span>
                </div>
                <p className="text-[10px] text-slate-400 mt-1 line-clamp-2">{ag.role}</p>
                <div className="mt-2 flex items-center justify-between text-[10px]">
                  <span className="text-emerald-400 font-bold">{ag.confidence}%</span>
                  <span className="text-slate-500">{ag.lastRun}</span>
                </div>
              </div>
            );
          })}
        </div>

        {/* Connector Lines */}
        <div className="flex justify-center -my-2">
          <ArrowDown className="w-6 h-6 text-slate-600 animate-bounce" />
        </div>

        {/* Level 3: Action Planner & Execution Agent */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 max-w-xl mx-auto">
          {agents.slice(6, 8).map((ag) => {
            const isSelected = selectedAgent.id === ag.id;
            return (
              <div
                key={ag.id}
                onClick={() => setSelectedAgent(ag)}
                className={`p-4 rounded-2xl border-2 cursor-pointer transition-all ${
                  isSelected
                    ? 'border-sky-400 bg-sky-950/40 ring-4 ring-sky-500/20'
                    : 'border-slate-800 bg-slate-900/80 hover:border-slate-700'
                }`}
              >
                <div className="flex items-center gap-2">
                  {getAgentIcon(ag.id)}
                  <span className="font-bold text-xs text-white">{ag.name}</span>
                </div>
                <p className="text-[11px] text-slate-400 mt-1">{ag.role}</p>
                <div className="mt-2 flex items-center justify-between text-[10px]">
                  <span className="text-sky-400 font-bold">Confidence {ag.confidence}%</span>
                  <span className="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300">{t("common.active", "Active")}</span>
                </div>
              </div>
            );
          })}
        </div>

      </div>

      {/* Selected Agent Inspector & Real-Time Log Stream */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {selectedAgent && (
          <div className="lg:col-span-7 bg-white p-6 rounded-3xl border border-slate-200/80 shadow-card-soft space-y-4">
            <div className="flex items-start justify-between">
              <div className="flex items-center gap-3">
                <div className="p-3 rounded-2xl bg-slate-100">
                  {getAgentIcon(selectedAgent.id)}
                </div>
                <div>
                  <h3 className="text-base font-bold text-slate-900">{selectedAgent.name}</h3>
                  <p className="text-xs text-slate-500">{selectedAgent.role}</p>
                </div>
              </div>

              <span className="px-2.5 py-1 rounded-full text-xs font-extrabold bg-emerald-50 text-emerald-700 border border-emerald-200">
                {t("common.confidence", "Confidence")}: {selectedAgent.confidence}%
              </span>
            </div>

            <div className="p-4 rounded-2xl bg-slate-50 border border-slate-100 text-xs">
              <span className="text-slate-400 text-[10px] uppercase font-bold block mb-1">
                {t("agentsPage.activeReasoning", "Active Reasoning Task")}
              </span>
              <p className="font-bold text-slate-800 text-sm leading-relaxed">
                "{selectedAgent.currentTask}"
              </p>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
              <div className="p-3.5 rounded-2xl bg-slate-50 border border-slate-100 space-y-2">
                <span className="font-bold text-slate-700 block text-[11px] uppercase tracking-wider">
                  📥 {t("agentsPage.ingestedInputs", "Ingested Inputs:")}
                </span>
                <ul className="space-y-1 text-slate-600">
                  {selectedAgent.inputs.map((inp, idx) => (
                    <li key={idx} className="flex items-center gap-1.5">
                      <span className="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
                      <span>{inp}</span>
                    </li>
                  ))}
                </ul>
              </div>

              <div className="p-3.5 rounded-2xl bg-slate-50 border border-slate-100 space-y-2">
                <span className="font-bold text-slate-700 block text-[11px] uppercase tracking-wider">
                  📤 {t("agentsPage.generatedOutputs", "Generated Outputs:")}
                </span>
                <ul className="space-y-1 text-slate-600">
                  {selectedAgent.outputs.map((out, idx) => (
                    <li key={idx} className="flex items-center gap-1.5">
                      <span className="w-1.5 h-1.5 rounded-full bg-purple-500"></span>
                      <span>{out}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>

          </div>
        )}

        <div className="lg:col-span-5 bg-slate-900 p-5 rounded-3xl border border-slate-800 shadow-xl text-white space-y-3 font-mono text-xs">
          <div className="flex items-center justify-between pb-2 border-b border-slate-800">
            <span className="flex items-center gap-2 text-slate-300 font-bold">
              <Terminal className="w-4 h-4 text-emerald-400" />
              {t("agentsPage.eventStream", "Agent Audit Log Stream")}
            </span>
            <span className="text-[10px] text-emerald-400 animate-pulse">● LIVE</span>
          </div>

          <div className="space-y-3 max-h-72 overflow-y-auto pr-1">
            {activityLogs.map((log) => (
              <div key={log.id} className="p-2.5 rounded-xl bg-slate-800/80 border border-slate-700/60 text-[11px] space-y-1">
                <div className="flex items-center justify-between text-slate-400">
                  <span className="text-emerald-400 font-bold">{log.agent}</span>
                  <span>{log.time}</span>
                </div>
                <p className="text-slate-200">{log.event}</p>
              </div>
            ))}
          </div>
        </div>

      </div>

    </div>
  );
}
