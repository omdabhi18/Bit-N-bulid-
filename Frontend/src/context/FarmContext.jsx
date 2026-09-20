import React, { createContext, useContext, useState, useEffect } from 'react';
import {
  initialFarmProfile,
  currentTelemetry,
  fieldsData,
  hardwareSensors,
  detectedRisks,
  aiAdvisories,
  initialActionPlans,
  initialTasks,
  aiAgents,
  weatherForecast,
  auditActivityLog,
  escalationTickets
} from '../data/mockFarmData';
import confetti from 'canvas-confetti';

const FarmContext = createContext();

export function FarmProvider({ children }) {
  const [profile, setProfile] = useState(initialFarmProfile);
  const [telemetry, setTelemetry] = useState(currentTelemetry);
  const [fields, setFields] = useState(fieldsData);
  const [selectedFieldId, setSelectedFieldId] = useState("field-a");
  const [sensors, setSensors] = useState(hardwareSensors);
  const [risks, setRisks] = useState(detectedRisks);
  const [advisories, setAdvisories] = useState(aiAdvisories);
  const [actionPlans, setActionPlans] = useState(initialActionPlans);
  const [tasks, setTasks] = useState(initialTasks);
  const [agents, setAgents] = useState(aiAgents);
  const [activityLogs, setActivityLogs] = useState(auditActivityLog);
  const [escalations, setEscalations] = useState(escalationTickets);
  const [toastMessage, setToastMessage] = useState(null);
  const [activeValve, setActiveValve] = useState({ fieldA: false, fieldB: false, fieldC: false });

  // Helper to show pleasant toast notifications
  const showToast = (message, type = 'success') => {
    setToastMessage({ text: message, type });
    setTimeout(() => {
      setToastMessage(null);
    }, 4000);
  };

  // Trigger automated Solenoid Drip Valve (IoT execution simulation)
  const triggerIrrigationValve = (fieldId, minutes = 35) => {
    setActiveValve(prev => ({
      ...prev,
      [fieldId === 'field-a' ? 'fieldA' : fieldId === 'field-b' ? 'fieldB' : 'fieldC']: true
    }));

    // Add activity log
    const newLog = {
      id: `LOG-${Date.now()}`,
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      agent: "Execution Agent",
      event: `⚡ Solenoid Valve opened for ${fieldId.toUpperCase()} (${minutes} min run scheduled)`,
      severity: "success"
    };
    setActivityLogs(prev => [newLog, ...prev]);

    // Update telemetry: moisture goes up gradually
    setTimeout(() => {
      setTelemetry(prev => ({
        ...prev,
        soilMoisture: Math.min(50, prev.soilMoisture + 4.5),
        soilMoistureStatus: "Optimal (પૂરતો ભેજ)"
      }));
    }, 2500);

    confetti({
      particleCount: 50,
      spread: 60,
      origin: { y: 0.8 }
    });

    showToast(`Drip Irrigation Valve activated for ${fieldId.toUpperCase()}! 💧 Running for ${minutes} mins.`);
  };

  const stopIrrigationValve = (fieldId) => {
    setActiveValve(prev => ({
      ...prev,
      [fieldId === 'field-a' ? 'fieldA' : fieldId === 'field-b' ? 'fieldB' : 'fieldC']: false
    }));
    showToast(`Irrigation shut down for ${fieldId.toUpperCase()}.`);
  };

  // Approve AI Advisory
  const approveAdvisory = (advisoryId) => {
    setAdvisories(prev => prev.map(a => {
      if (a.id === advisoryId) {
        return { ...a, status: "Approved" };
      }
      return a;
    }));

    const adv = advisories.find(a => a.id === advisoryId);
    if (adv) {
      const newLog = {
        id: `LOG-${Date.now()}`,
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        agent: "Farmer Interaction",
        event: `Farmer approved recommendation: "${adv.title}"`,
        severity: "success"
      };
      setActivityLogs(prev => [newLog, ...prev]);
    }

    confetti({ particleCount: 40, spread: 50, origin: { y: 0.7 } });
    showToast("Advisory approved! Added to scheduled execution pipeline.");
  };

  // Reject Advisory with reason
  const rejectAdvisory = (advisoryId, reason = "Farmer decided to delay") => {
    setAdvisories(prev => prev.map(a => {
      if (a.id === advisoryId) {
        return { ...a, status: "Rejected" };
      }
      return a;
    }));

    const newLog = {
      id: `LOG-${Date.now()}`,
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      agent: "Farmer Interaction",
      event: `Farmer dismissed advisory #${advisoryId}: Reason - ${reason}`,
      severity: "warning"
    };
    setActivityLogs(prev => [newLog, ...prev]);
    showToast("Advisory dismissed and logged.", "warning");
  };

  // Generate Action Plan from Risk
  const generatePlanFromRisk = (risk) => {
    const newPlanId = `PLAN-${Math.floor(1000 + Math.random() * 9000)}`;
    const newPlan = {
      id: newPlanId,
      title: `${risk.category} Mitigation Plan`,
      targetField: risk.field,
      actionType: risk.recommendedAction,
      scheduledTime: "Today • 18:00 IST",
      status: "Draft",
      priority: risk.severity,
      estimatedCost: 150,
      waterVolume: "1,500 L",
      constraints: {
        costBudget: "Max ₹250",
        weatherWindow: "Safe Window (Wind < 15 km/h)",
        waterAvailability: "Adequate Level (88%)",
        safetyProtocols: "Standard field PPE"
      },
      hardwareTarget: "Zone Drip & Sprayer Node",
      assignedTo: profile.farmerName
    };

    setActionPlans(prev => [newPlan, ...prev]);
    setRisks(prev => prev.map(r => r.id === risk.id ? { ...r, planGenerated: true, planId: newPlanId } : r));

    showToast(`Action Plan ${newPlanId} successfully generated by Constrained Planner Agent!`);
    return newPlanId;
  };

  // Approve Action Plan
  const approvePlan = (planId) => {
    setActionPlans(prev => prev.map(p => {
      if (p.id === planId) {
        return { ...p, status: "Approved" };
      }
      return p;
    }));

    const targetPlan = actionPlans.find(p => p.id === planId);
    if (targetPlan) {
      // Also automatically create task on Kanban board
      const newTask = {
        id: `TSK-${Date.now()}`,
        title: targetPlan.actionType,
        field: targetPlan.targetField,
        planId: targetPlan.id,
        status: "todo",
        priority: targetPlan.priority,
        dueTime: targetPlan.scheduledTime,
        assignedTo: targetPlan.assignedTo,
        icon: "CheckCircle",
        notes: `Auto-dispatched from approved plan ${planId}`
      };
      setTasks(prev => [newTask, ...prev]);
    }

    confetti({ particleCount: 60, spread: 70, origin: { y: 0.7 } });
    showToast(`Plan ${planId} approved! Dispatched to Task Execution board.`);
  };

  // Move task status (Kanban)
  const moveTask = (taskId, newStatus) => {
    setTasks(prev => prev.map(t => {
      if (t.id === taskId) {
        return { ...t, status: newStatus };
      }
      return t;
    }));

    if (newStatus === 'completed') {
      confetti({ particleCount: 35, spread: 45, origin: { y: 0.6 } });
      showToast("Task completed! Telemetry feedback updated.");
    }
  };

  // Add Task
  const addTask = (task) => {
    setTasks(prev => [{ ...task, id: `TSK-${Date.now()}` }, ...prev]);
    showToast("New field task added to board.");
  };

  // Submit Escalation to Agronomist
  const submitEscalation = (ticket) => {
    const newId = `ESC-${Math.floor(100 + Math.random() * 900)}`;
    const newTicket = {
      ...ticket,
      id: newId,
      status: "Review Pending",
      submittedAt: "Just now"
    };
    setEscalations(prev => [newTicket, ...prev]);
    showToast(`Escalation #${newId} dispatched to Senior University Agronomist.`);
  };

  const selectedField = fields.find(f => f.id === selectedFieldId) || fields[0];

  return (
    <FarmContext.Provider value={{
      profile,
      setProfile,
      telemetry,
      setTelemetry,
      fields,
      setFields,
      selectedFieldId,
      setSelectedFieldId,
      selectedField,
      sensors,
      risks,
      advisories,
      actionPlans,
      tasks,
      agents,
      activityLogs,
      escalations,
      weatherForecast,
      activeValve,
      triggerIrrigationValve,
      stopIrrigationValve,
      approveAdvisory,
      rejectAdvisory,
      generatePlanFromRisk,
      approvePlan,
      moveTask,
      addTask,
      submitEscalation,
      showToast
    }}>
      {children}
      {toastMessage && (
        <div className={`fixed bottom-6 right-6 z-50 flex items-center gap-3 px-5 py-3.5 rounded-2xl shadow-xl text-white font-medium text-sm transition-all transform animate-bounce ${
          toastMessage.type === 'warning' ? 'bg-amber-600' : 'bg-emerald-600'
        }`}>
          <span>{toastMessage.type === 'warning' ? '⚠️' : '✅'}</span>
          <span>{toastMessage.text}</span>
        </div>
      )}
    </FarmContext.Provider>
  );
}

export const useFarm = () => useContext(FarmContext);
