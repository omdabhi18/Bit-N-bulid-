import React, { useState } from 'react';
import { useFarm } from '../context/FarmContext';
import { useLanguage } from '../context/LanguageContext';
import VoiceSpeaker from '../components/common/VoiceSpeaker';
import {
  CheckSquare,
  Play,
  CheckCircle2,
  Plus,
  Droplets,
  ArrowRight
} from 'lucide-react';

export default function TaskExecutionPage() {
  const { tasks, moveTask, addTask, triggerIrrigationValve, activeValve } = useFarm();
  const { t, language } = useLanguage();
  const [showAddModal, setShowAddModal] = useState(false);
  const [newTaskTitle, setNewTaskTitle] = useState('');
  const [newTaskField, setNewTaskField] = useState('Field A');
  const [newTaskPriority, setNewTaskPriority] = useState('High');

  const todoTasks = tasks.filter(t => t.status === 'todo');
  const inProgressTasks = tasks.filter(t => t.status === 'in-progress');
  const completedTasks = tasks.filter(t => t.status === 'completed');

  const handleCreateTask = (e) => {
    e.preventDefault();
    if (!newTaskTitle.trim()) return;

    addTask({
      title: newTaskTitle,
      field: newTaskField,
      status: 'todo',
      priority: newTaskPriority,
      dueTime: 'Today • 18:00',
      assignedTo: 'Kishanbhai Patel',
      icon: 'CheckCircle',
      notes: 'Custom task scheduled by farmer'
    });

    setNewTaskTitle('');
    setShowAddModal(false);
  };

  return (
    <div className="space-y-6">
      
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-white p-5 rounded-3xl border border-slate-200 shadow-card-soft">
        <div>
          <div className="flex items-center gap-2">
            <span className="p-2 rounded-xl bg-emerald-100 text-emerald-800">
              <CheckSquare className="w-5 h-5" />
            </span>
            <div>
              <h1 className="text-xl sm:text-2xl font-extrabold text-slate-900 tracking-tight">
                {t("tasksPage.title", "Task Execution & Automated Workflow Board")}
              </h1>
              <p className="text-xs text-slate-500">
                {t("tasksPage.subtitle", "Kanban tracking for IoT automated jobs, worker field assignments, and scouting inspections")}
              </p>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={() => setShowAddModal(true)}
            className="px-4 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 text-white text-xs font-bold flex items-center gap-1.5 transition-all"
          >
            <Plus className="w-4 h-4" />
            <span>{t("tasksPage.addFieldTask", "Add Field Task")}</span>
          </button>

          <VoiceSpeaker
            text={language === 'gu'
              ? `કામગીરી બોર્ડ. કરવાના કામો ${todoTasks.length} બાકી છે, અને ${inProgressTasks.length} ચાલુ છે. ડ્રિપ પિયત બટન દબાવીને સીધું ચાલુ કરી શકો છો.`
              : `Task execution board. There are ${todoTasks.length} pending tasks to do, and ${inProgressTasks.length} in progress. Drip irrigation can be triggered automatically.`}
            label={t("tasksPage.listenTasks", "Listen Tasks")}
          />
        </div>
      </div>

      {/* Hardware Automation Solenoid Quick Trigger Banner */}
      <div className="bg-gradient-to-r from-sky-900 via-slate-900 to-emerald-950 p-5 rounded-3xl text-white shadow-xl flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="w-12 h-12 rounded-2xl bg-sky-500/20 border border-sky-400/40 flex items-center justify-center text-sky-400">
            <Droplets className="w-6 h-6 animate-bounce" />
          </div>
          <div>
            <span className="text-[10px] font-bold uppercase tracking-wider text-sky-400 bg-sky-950/60 px-2 py-0.5 rounded border border-sky-800">
              IoT Drip Solenoid Actuator SV-01
            </span>
            <h3 className="text-base font-bold text-white mt-1">
              {t("tasksPage.dripValveHeading", "Field A Drip Automation Valve")}
            </h3>
            <p className="text-xs text-slate-300">
              {t("tasksPage.dripValveSub", "Scheduled for 18:00 IST (35 mins • 2,500 L water • ₹45 electricity)")}
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={() => triggerIrrigationValve('field-a', 35)}
            className={`px-5 py-2.5 rounded-xl text-xs font-bold transition-all flex items-center gap-2 shadow-lg ${
              activeValve.fieldA
                ? 'bg-sky-500 text-white animate-pulse'
                : 'bg-emerald-500 hover:bg-emerald-400 text-slate-950'
            }`}
          >
            <Play className="w-4 h-4 fill-current" />
            <span>{activeValve.fieldA ? t("dashboard.valveRunning", "Valve Running (35m)") : t("tasksPage.triggerValveLive", "Trigger Valve Now (Live Test)")}</span>
          </button>
        </div>
      </div>

      {/* Kanban Board Columns: TO DO, IN PROGRESS, COMPLETED */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
        
        {/* TO DO COLUMN */}
        <div className="bg-slate-100/70 p-4 rounded-3xl border border-slate-200/80 space-y-3">
          <div className="flex items-center justify-between px-1">
            <div className="flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full bg-amber-500"></span>
              <h3 className="font-bold text-slate-900 text-sm">{t("tasksPage.todoCol", "TO DO (Pending)")}</h3>
            </div>
            <span className="text-xs font-extrabold px-2 py-0.5 rounded-full bg-amber-100 text-amber-800">
              {todoTasks.length}
            </span>
          </div>

          <div className="space-y-3">
            {todoTasks.map((task) => (
              <div
                key={task.id}
                className="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm hover:shadow-md transition-all space-y-2.5"
              >
                <div className="flex items-center justify-between">
                  <span className="text-[10px] font-extrabold uppercase px-2 py-0.5 rounded bg-amber-50 text-amber-800 border border-amber-200">
                    {task.priority}
                  </span>
                  <span className="text-[11px] font-semibold text-slate-400">{task.field}</span>
                </div>

                <h4 className="text-xs font-bold text-slate-900 leading-snug">{task.title}</h4>
                <p className="text-[11px] text-slate-500">{task.notes}</p>

                <div className="pt-2 border-t border-slate-100 flex items-center justify-between text-[11px]">
                  <span className="text-slate-500 font-medium">Due: {task.dueTime}</span>
                  <button
                    onClick={() => moveTask(task.id, 'in-progress')}
                    className="px-2.5 py-1 rounded-lg bg-emerald-50 hover:bg-emerald-100 text-emerald-700 font-bold flex items-center gap-1 transition-colors"
                  >
                    <span>{t("common.start", "Start")}</span>
                    <ArrowRight className="w-3 h-3" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* IN PROGRESS COLUMN */}
        <div className="bg-slate-100/70 p-4 rounded-3xl border border-slate-200/80 space-y-3">
          <div className="flex items-center justify-between px-1">
            <div className="flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full bg-sky-500 animate-pulse"></span>
              <h3 className="font-bold text-slate-900 text-sm">{t("tasksPage.inProgressCol", "IN PROGRESS")}</h3>
            </div>
            <span className="text-xs font-extrabold px-2 py-0.5 rounded-full bg-sky-100 text-sky-800">
              {inProgressTasks.length}
            </span>
          </div>

          <div className="space-y-3">
            {inProgressTasks.map((task) => (
              <div
                key={task.id}
                className="bg-white p-4 rounded-2xl border-2 border-sky-300 shadow-md space-y-2.5"
              >
                <div className="flex items-center justify-between">
                  <span className="text-[10px] font-extrabold uppercase px-2 py-0.5 rounded bg-sky-50 text-sky-800 border border-sky-200">
                    {t("common.inProgress", "Active")}
                  </span>
                  <span className="text-[11px] font-semibold text-slate-400">{task.field}</span>
                </div>

                <h4 className="text-xs font-bold text-slate-900 leading-snug">{task.title}</h4>
                <p className="text-[11px] text-slate-500">{task.notes}</p>

                <div className="pt-2 border-t border-slate-100 flex items-center justify-between text-[11px]">
                  <span className="text-slate-500 font-medium">{task.assignedTo}</span>
                  <button
                    onClick={() => moveTask(task.id, 'completed')}
                    className="px-3 py-1 rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white font-bold flex items-center gap-1 transition-colors"
                  >
                    <CheckCircle2 className="w-3.5 h-3.5" />
                    <span>{t("common.complete", "Complete")}</span>
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* COMPLETED COLUMN */}
        <div className="bg-slate-100/70 p-4 rounded-3xl border border-slate-200/80 space-y-3">
          <div className="flex items-center justify-between px-1">
            <div className="flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full bg-emerald-500"></span>
              <h3 className="font-bold text-slate-900 text-sm">{t("tasksPage.completedCol", "COMPLETED")}</h3>
            </div>
            <span className="text-xs font-extrabold px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-800">
              {completedTasks.length}
            </span>
          </div>

          <div className="space-y-3">
            {completedTasks.map((task) => (
              <div
                key={task.id}
                className="bg-white/80 p-4 rounded-2xl border border-slate-200 space-y-2 opacity-85"
              >
                <div className="flex items-center justify-between">
                  <span className="text-[10px] font-extrabold uppercase px-2 py-0.5 rounded bg-emerald-50 text-emerald-800">
                    {t("common.completed", "Done")}
                  </span>
                  <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                </div>

                <h4 className="text-xs font-bold text-slate-800 line-through">{task.title}</h4>
                <p className="text-[11px] text-slate-400">{task.notes}</p>
                <span className="text-[10px] text-slate-400 block pt-1 border-t border-slate-100">
                  {task.assignedTo}
                </span>
              </div>
            ))}
          </div>
        </div>

      </div>

      {/* Add Task Modal */}
      {showAddModal && (
        <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-white rounded-3xl p-6 max-w-md w-full shadow-2xl border border-slate-200 animate-in fade-in zoom-in-95">
            <h3 className="text-base font-bold text-slate-900">{t("tasksPage.scheduleModalTitle", "Schedule Field Task")}</h3>
            <p className="text-xs text-slate-500 mt-0.5">{t("tasksPage.scheduleModalSub", "Assign an irrigation, spraying or scouting action")}</p>

            <form onSubmit={handleCreateTask} className="mt-4 space-y-3 text-xs">
              <div>
                <label className="font-bold text-slate-700 block mb-1">{t("tasksPage.taskDesc", "Task Description")}</label>
                <input
                  type="text"
                  value={newTaskTitle}
                  onChange={(e) => setNewTaskTitle(e.target.value)}
                  placeholder="e.g. Inspect Field B for aphid clusters"
                  className="w-full p-2.5 rounded-xl border border-slate-200 focus:outline-none focus:border-emerald-500"
                  required
                />
              </div>

              <div>
                <label className="font-bold text-slate-700 block mb-1">{t("tasksPage.fieldPlot", "Field Plot")}</label>
                <select
                  value={newTaskField}
                  onChange={(e) => setNewTaskField(e.target.value)}
                  className="w-full p-2.5 rounded-xl border border-slate-200 focus:outline-none focus:border-emerald-500"
                >
                  <option value="Field A">Field A (BT Cotton)</option>
                  <option value="Field B">Field B (Wheat)</option>
                  <option value="Field C">Field C (Groundnut)</option>
                </select>
              </div>

              <div>
                <label className="font-bold text-slate-700 block mb-1">{t("common.priority", "Priority")}</label>
                <select
                  value={newTaskPriority}
                  onChange={(e) => setNewTaskPriority(e.target.value)}
                  className="w-full p-2.5 rounded-xl border border-slate-200 focus:outline-none focus:border-emerald-500"
                >
                  <option value="High">High</option>
                  <option value="Normal">Normal</option>
                  <option value="Low">Low</option>
                </select>
              </div>

              <div className="pt-3 flex justify-end gap-2">
                <button
                  type="button"
                  onClick={() => setShowAddModal(false)}
                  className="px-4 py-2 rounded-xl text-slate-600 font-bold hover:bg-slate-100"
                >
                  {t("common.cancel", "Cancel")}
                </button>
                <button
                  type="submit"
                  className="px-5 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-bold"
                >
                  {t("tasksPage.saveTask", "Save Task")}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

    </div>
  );
}
