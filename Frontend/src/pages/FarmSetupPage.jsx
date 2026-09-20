import React, { useState } from 'react';
import { useFarm } from '../context/FarmContext';
import { useLanguage } from '../context/LanguageContext';
import VoiceSpeaker from '../components/common/VoiceSpeaker';
import {
  Settings2,
  User,
  MapPin,
  Sprout,
  Radio,
  Save,
  Plus
} from 'lucide-react';

export default function FarmSetupPage() {
  const { profile, setProfile, sensors, showToast } = useFarm();
  const { t } = useLanguage();

  const [formData, setFormData] = useState({ ...profile });
  const [activeTab, setActiveTab] = useState('farmer'); // farmer, farm, crops, sensors

  const handleSave = (e) => {
    e.preventDefault();
    setProfile(formData);
    showToast("Farm profile and field parameters saved successfully!");
  };

  return (
    <div className="space-y-6">
      
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-white p-5 rounded-3xl border border-slate-200 shadow-card-soft">
        <div>
          <div className="flex items-center gap-2">
            <span className="p-2 rounded-xl bg-slate-100 text-slate-800">
              <Settings2 className="w-5 h-5" />
            </span>
            <div>
              <h1 className="text-xl sm:text-2xl font-extrabold text-slate-900 tracking-tight">
                {t("setupPage.title", "Farm Setup & IoT Sensor Configuration")}
              </h1>
              <p className="text-xs text-slate-500">
                {t("setupPage.subtitle", "Configure your holding details, soil type, irrigation layout, and connect physical edge sensors")}
              </p>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <VoiceSpeaker
            text="Farm setup and profile page. Customize your farm acreage, soil characteristics, and connect IoT sensors to receive tailored multi-agent agricultural advisories."
            label={t("setupPage.listenGuide", "Listen Guide")}
          />
        </div>
      </div>

      {/* Tab Navigation */}
      <div className="flex flex-wrap gap-2 border-b border-slate-200 pb-2">
        <button
          onClick={() => setActiveTab('farmer')}
          className={`px-4 py-2 rounded-2xl text-xs font-bold transition-all flex items-center gap-1.5 ${
            activeTab === 'farmer' ? 'bg-emerald-600 text-white shadow-sm' : 'bg-white text-slate-600 hover:bg-slate-100'
          }`}
        >
          <User className="w-4 h-4" />
          <span>{t("setupPage.tabFarmer", "1. Farmer Profile")}</span>
        </button>

        <button
          onClick={() => setActiveTab('farm')}
          className={`px-4 py-2 rounded-2xl text-xs font-bold transition-all flex items-center gap-1.5 ${
            activeTab === 'farm' ? 'bg-emerald-600 text-white shadow-sm' : 'bg-white text-slate-600 hover:bg-slate-100'
          }`}
        >
          <MapPin className="w-4 h-4" />
          <span>{t("setupPage.tabFarm", "2. Farm & Soil Details")}</span>
        </button>

        <button
          onClick={() => setActiveTab('crops')}
          className={`px-4 py-2 rounded-2xl text-xs font-bold transition-all flex items-center gap-1.5 ${
            activeTab === 'crops' ? 'bg-emerald-600 text-white shadow-sm' : 'bg-white text-slate-600 hover:bg-slate-100'
          }`}
        >
          <Sprout className="w-4 h-4" />
          <span>{t("setupPage.tabCrops", "3. Crops & Phenology")}</span>
        </button>

        <button
          onClick={() => setActiveTab('sensors')}
          className={`px-4 py-2 rounded-2xl text-xs font-bold transition-all flex items-center gap-1.5 ${
            activeTab === 'sensors' ? 'bg-emerald-600 text-white shadow-sm' : 'bg-white text-slate-600 hover:bg-slate-100'
          }`}
        >
          <Radio className="w-4 h-4" />
          <span>{t("setupPage.tabSensors", "4. IoT Sensors Fleet")}</span>
        </button>
      </div>

      {/* Form Container */}
      <form onSubmit={handleSave} className="bg-white p-6 rounded-3xl border border-slate-200 shadow-card-soft space-y-6">
        
        {/* Tab 1: Farmer Information */}
        {activeTab === 'farmer' && (
          <div className="space-y-4 text-xs">
            <h3 className="text-sm font-bold text-slate-900 border-b pb-2">Farmer Identification</h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="font-bold text-slate-700 block mb-1">Farmer Full Name</label>
                <input
                  type="text"
                  value={formData.farmerName}
                  onChange={(e) => setFormData({ ...formData, farmerName: e.target.value })}
                  className="w-full p-2.5 rounded-xl border border-slate-200 focus:outline-none focus:border-emerald-500"
                  required
                />
              </div>

              <div>
                <label className="font-bold text-slate-700 block mb-1">Village</label>
                <input
                  type="text"
                  value={formData.village}
                  onChange={(e) => setFormData({ ...formData, village: e.target.value })}
                  className="w-full p-2.5 rounded-xl border border-slate-200 focus:outline-none focus:border-emerald-500"
                  required
                />
              </div>

              <div>
                <label className="font-bold text-slate-700 block mb-1">Taluka</label>
                <input
                  type="text"
                  value={formData.taluka}
                  onChange={(e) => setFormData({ ...formData, taluka: e.target.value })}
                  className="w-full p-2.5 rounded-xl border border-slate-200 focus:outline-none focus:border-emerald-500"
                  required
                />
              </div>

              <div>
                <label className="font-bold text-slate-700 block mb-1">District & State</label>
                <input
                  type="text"
                  value={`${formData.district}, ${formData.state}`}
                  readOnly
                  className="w-full p-2.5 rounded-xl border border-slate-200 bg-slate-50 text-slate-600"
                />
              </div>
            </div>
          </div>
        )}

        {/* Tab 2: Farm Information */}
        {activeTab === 'farm' && (
          <div className="space-y-4 text-xs">
            <h3 className="text-sm font-bold text-slate-900 border-b pb-2">Holding & Soil Characteristics</h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="font-bold text-slate-700 block mb-1">Farm Name</label>
                <input
                  type="text"
                  value={formData.farmName}
                  onChange={(e) => setFormData({ ...formData, farmName: e.target.value })}
                  className="w-full p-2.5 rounded-xl border border-slate-200 focus:outline-none focus:border-emerald-500"
                  required
                />
              </div>

              <div>
                <label className="font-bold text-slate-700 block mb-1">Total Holding Area (Acres)</label>
                <input
                  type="number"
                  step="0.1"
                  value={formData.totalAreaAcre}
                  onChange={(e) => setFormData({ ...formData, totalAreaAcre: parseFloat(e.target.value) })}
                  className="w-full p-2.5 rounded-xl border border-slate-200 focus:outline-none focus:border-emerald-500"
                  required
                />
              </div>

              <div>
                <label className="font-bold text-slate-700 block mb-1">Soil Taxonomy & Texture</label>
                <input
                  type="text"
                  value={formData.soilType}
                  onChange={(e) => setFormData({ ...formData, soilType: e.target.value })}
                  className="w-full p-2.5 rounded-xl border border-slate-200 focus:outline-none focus:border-emerald-500"
                  required
                />
              </div>

              <div>
                <label className="font-bold text-slate-700 block mb-1">Primary Irrigation System</label>
                <input
                  type="text"
                  value={formData.irrigationMethod}
                  onChange={(e) => setFormData({ ...formData, irrigationMethod: e.target.value })}
                  className="w-full p-2.5 rounded-xl border border-slate-200 focus:outline-none focus:border-emerald-500"
                  required
                />
              </div>
            </div>
          </div>
        )}

        {/* Tab 3: Crops */}
        {activeTab === 'crops' && (
          <div className="space-y-4 text-xs">
            <h3 className="text-sm font-bold text-slate-900 border-b pb-2">Active Crops & Growth Stages</h3>
            <div className="space-y-3">
              {formData.crops.map((c, idx) => (
                <div key={idx} className="p-4 rounded-2xl bg-slate-50 border border-slate-200 grid grid-cols-2 sm:grid-cols-4 gap-3">
                  <div>
                    <span className="text-slate-400 block text-[10px]">Crop & Variety</span>
                    <span className="font-extrabold text-slate-900 text-xs">{c.name} ({c.variety})</span>
                  </div>
                  <div>
                    <span className="text-slate-400 block text-[10px]">Field & Acreage</span>
                    <span className="font-bold text-slate-800">{c.field} • {c.area} Acres</span>
                  </div>
                  <div>
                    <span className="text-slate-400 block text-[10px]">Current Stage</span>
                    <span className="font-bold text-emerald-700">{c.stage}</span>
                  </div>
                  <div>
                    <span className="text-slate-400 block text-[10px]">Sowing Date</span>
                    <span className="text-slate-600">{c.sowingDate}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Tab 4: Sensors */}
        {activeTab === 'sensors' && (
          <div className="space-y-4 text-xs">
            <div className="flex items-center justify-between border-b pb-2">
              <h3 className="text-sm font-bold text-slate-900">Connected IoT Sensor Hardware Nodes</h3>
              <button
                type="button"
                onClick={() => alert("Auto-pairing mode initiated. Turn on your LoRa/BLE probe to pair.")}
                className="px-3 py-1.5 rounded-xl bg-emerald-50 text-emerald-700 font-bold border border-emerald-200 flex items-center gap-1"
              >
                <Plus className="w-3.5 h-3.5" />
                <span>Pair New Sensor</span>
              </button>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              {sensors.map((s) => (
                <div key={s.id} className="p-4 rounded-2xl bg-slate-50 border border-slate-200 space-y-1">
                  <div className="flex items-center justify-between">
                    <span className="font-extrabold text-slate-900">{s.id} ({s.name})</span>
                    <span className="px-2 py-0.5 rounded bg-emerald-100 text-emerald-800 font-bold text-[10px]">
                      {s.status}
                    </span>
                  </div>
                  <p className="text-slate-500">{s.type}</p>
                  <p className="text-slate-400 text-[11px]">Location: {s.field} • Battery: {s.battery}% • Signal: {s.signal}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Submit Button */}
        <div className="pt-4 border-t border-slate-100 flex justify-end">
          <button
            type="submit"
            className="px-6 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs shadow-md shadow-emerald-500/20 flex items-center gap-2 transition-all"
          >
            <Save className="w-4 h-4" />
            <span>{t("setupPage.saveConfig", "Save Farm Configuration")}</span>
          </button>
        </div>

      </form>

    </div>
  );
}
