import React, { useState } from 'react';
import { useFarm } from '../../context/FarmContext';
import { useLanguage } from '../../context/LanguageContext';
import {
  Layers,
  MapPin,
  Droplets,
  Bug,
  Sprout,
  ZoomIn,
  ZoomOut,
  Radio
} from 'lucide-react';
import VoiceSpeaker from '../common/VoiceSpeaker';

export default function FarmMapbox({ onSelectField, activeLayerDefault = "all", height = "520px" }) {
  const { fields, selectedFieldId, setSelectedFieldId, activeValve, triggerIrrigationValve } = useFarm();
  const { t, language } = useLanguage();
  const [activeLayer, setActiveLayer] = useState(activeLayerDefault); // all, moisture, pest, sensors
  const [zoomLevel, setZoomLevel] = useState(1);
  const [useSatelliteMode, setUseSatelliteMode] = useState(false);

  const selectedField = fields.find(f => f.id === selectedFieldId) || fields[0];

  const handleFieldClick = (field) => {
    setSelectedFieldId(field.id);
    if (onSelectField) {
      onSelectField(field);
    }
  };

  return (
    <div className="relative w-full bg-slate-900 rounded-3xl overflow-hidden shadow-xl border border-slate-700/60" style={{ height }}>
      
      {/* Top Map Toolbar */}
      <div className="absolute top-4 left-4 right-4 z-20 flex flex-wrap items-center justify-between gap-2 pointer-events-none">
        
        {/* Layer Filters */}
        <div className="flex items-center gap-1 bg-slate-900/90 backdrop-blur-md p-1.5 rounded-2xl border border-slate-700 pointer-events-auto shadow-lg">
          <button
            onClick={() => setActiveLayer('all')}
            className={`px-3 py-1.5 rounded-xl text-xs font-semibold transition-all ${
              activeLayer === 'all' ? 'bg-emerald-600 text-white shadow' : 'text-slate-300 hover:text-white'
            }`}
          >
            {t("mapPage.allLayers", "All Layers")}
          </button>
          <button
            onClick={() => setActiveLayer('moisture')}
            className={`px-3 py-1.5 rounded-xl text-xs font-semibold flex items-center gap-1.5 transition-all ${
              activeLayer === 'moisture' ? 'bg-amber-600 text-white shadow' : 'text-slate-300 hover:text-white'
            }`}
          >
            <Droplets className="w-3.5 h-3.5" />
            <span>{t("mapPage.waterStress", "Water Stress")}</span>
          </button>
          <button
            onClick={() => setActiveLayer('pest')}
            className={`px-3 py-1.5 rounded-xl text-xs font-semibold flex items-center gap-1.5 transition-all ${
              activeLayer === 'pest' ? 'bg-rose-600 text-white shadow' : 'text-slate-300 hover:text-white'
            }`}
          >
            <Bug className="w-3.5 h-3.5" />
            <span>{t("mapPage.pestDanger", "Pest Danger")}</span>
          </button>
          <button
            onClick={() => setActiveLayer('sensors')}
            className={`px-3 py-1.5 rounded-xl text-xs font-semibold flex items-center gap-1.5 transition-all ${
              activeLayer === 'sensors' ? 'bg-sky-600 text-white shadow' : 'text-slate-300 hover:text-white'
            }`}
          >
            <Radio className="w-3.5 h-3.5" />
            <span>{t("mapPage.iotProbes", "IoT Probes")}</span>
          </button>
        </div>

        {/* Right Tools: Satellite Toggle & Zoom */}
        <div className="flex items-center gap-2 pointer-events-auto">
          <button
            onClick={() => setUseSatelliteMode(!useSatelliteMode)}
            className={`px-3 py-1.5 rounded-xl text-xs font-semibold backdrop-blur-md border transition-all ${
              useSatelliteMode
                ? 'bg-emerald-500 text-white border-emerald-400'
                : 'bg-slate-900/90 text-slate-300 border-slate-700 hover:text-white'
            }`}
          >
            {useSatelliteMode ? `🛰️ ${t("mapPage.satelliteView", "Satellite View")}` : `🗺️ ${t("mapPage.digitalTwin", "Digital Twin")}`}
          </button>

          <div className="flex items-center bg-slate-900/90 backdrop-blur-md border border-slate-700 rounded-2xl p-1">
            <button
              onClick={() => setZoomLevel(prev => Math.min(prev + 0.2, 1.8))}
              className="p-1.5 text-slate-300 hover:text-white hover:bg-slate-800 rounded-lg"
              title="Zoom In"
            >
              <ZoomIn className="w-4 h-4" />
            </button>
            <button
              onClick={() => setZoomLevel(prev => Math.max(prev - 0.2, 0.8))}
              className="p-1.5 text-slate-300 hover:text-white hover:bg-slate-800 rounded-lg"
              title="Zoom Out"
            >
              <ZoomOut className="w-4 h-4" />
            </button>
          </div>
        </div>

      </div>

      {/* Interactive Digital Twin Canvas / Vector Map Engine */}
      <div className="w-full h-full relative overflow-hidden flex items-center justify-center select-none bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950">
        
        {/* Background Grid */}
        <div
          className="absolute inset-0 opacity-15"
          style={{
            backgroundImage: `radial-gradient(#10b981 1px, transparent 1px), radial-gradient(#38bdf8 1px, transparent 1px)`,
            backgroundSize: '28px 28px',
            backgroundPosition: '0 0, 14px 14px'
          }}
        />

        {/* Interactive Farm Plots Graphic */}
        <div
          className="relative transition-transform duration-300 ease-out"
          style={{ transform: `scale(${zoomLevel})` }}
        >
          <svg viewBox="0 0 900 520" className="w-[850px] h-[480px] drop-shadow-2xl">
            <defs>
              <pattern id="soilTexture" width="20" height="20" patternUnits="userSpaceOnUse">
                <path d="M 0 10 L 20 10 M 10 0 L 10 20" stroke="#334155" strokeWidth="0.5" fill="none"/>
              </pattern>
              <linearGradient id="cottonGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor="#ca8a04" stopOpacity="0.85" />
                <stop offset="100%" stopColor="#eab308" stopOpacity="0.4" />
              </linearGradient>
              <linearGradient id="wheatGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor="#dc2626" stopOpacity="0.85" />
                <stop offset="100%" stopColor="#ef4444" stopOpacity="0.45" />
              </linearGradient>
              <linearGradient id="gnutGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor="#15803d" stopOpacity="0.85" />
                <stop offset="100%" stopColor="#22c55e" stopOpacity="0.45" />
              </linearGradient>
            </defs>

            {/* Farm Perimeter Fence line */}
            <rect
              x="60"
              y="40"
              width="780"
              height="440"
              rx="30"
              fill="#0f172a"
              stroke="#334155"
              strokeWidth="2"
              strokeDasharray="6 6"
            />

            {/* Internal Field Roads & Canal */}
            <path d="M 60 260 L 840 260" stroke="#475569" strokeWidth="12" strokeLinecap="round" />
            <path d="M 450 40 L 450 480" stroke="#475569" strokeWidth="12" strokeLinecap="round" />
            <path d="M 60 260 L 840 260" stroke="#0284c7" strokeWidth="3" strokeDasharray="8 4" />

            {/* FIELD A - BT COTTON (South-West) */}
            <g
              onClick={() => handleFieldClick(fields[0])}
              className="cursor-pointer transition-all group"
            >
              <path
                d="M 90 285 L 420 285 L 420 450 L 130 450 Q 90 450 90 410 Z"
                fill={activeLayer === 'pest' ? '#1e293b' : 'url(#cottonGrad)'}
                stroke={selectedFieldId === 'field-a' ? '#fbbf24' : '#eab308'}
                strokeWidth={selectedFieldId === 'field-a' ? '4' : '2'}
                className="transition-all hover:opacity-95"
              />
              <text x="140" y="340" fill="#ffffff" fontWeight="bold" fontSize="16" fontFamily="Outfit">
                {language === 'gu' ? 'ખેતર A: કપાસ' : language === 'hi' ? 'खेत A: कपास' : 'Field A: BT Cotton'}
              </text>
              <text x="140" y="365" fill="#fde047" fontSize="13" fontWeight="medium">
                5.2 Acres • {language === 'gu' ? 'ફૂલ અવસ્થા' : 'Flowering Stage'}
              </text>
              <text x="140" y="390" fill="#fef08a" fontSize="12">
                {t("metrics.soilMoisture", "Moisture")}: 31% ({t("metrics.deficit", "Water Stress")})
              </text>
            </g>

            {/* FIELD B - SHARBATI WHEAT (North-West) */}
            <g
              onClick={() => handleFieldClick(fields[1])}
              className="cursor-pointer transition-all group"
            >
              <path
                d="M 90 100 Q 90 65 130 65 L 420 65 L 420 235 L 90 235 Z"
                fill={activeLayer === 'moisture' ? '#1e293b' : 'url(#wheatGrad)'}
                stroke={selectedFieldId === 'field-b' ? '#f87171' : '#ef4444'}
                strokeWidth={selectedFieldId === 'field-b' ? '4' : '2'}
                className="transition-all hover:opacity-95"
              />
              <text x="140" y="125" fill="#ffffff" fontWeight="bold" fontSize="16" fontFamily="Outfit">
                {language === 'gu' ? 'ખેતર B: ઘઉં' : language === 'hi' ? 'खेत B: गेहूं' : 'Field B: Sharbati Wheat'}
              </text>
              <text x="140" y="150" fill="#fca5a5" fontSize="13" fontWeight="medium">
                4.1 Acres • {language === 'gu' ? 'કૂટ અવસ્થા' : 'Tillering Stage'}
              </text>
              <text x="140" y="175" fill="#fecaca" fontSize="12">
                {t("mapPage.pestDanger", "Pest Risk")} 78% • Low P
              </text>
            </g>

            {/* FIELD C - GROUNDNUT (East Zone) */}
            <g
              onClick={() => handleFieldClick(fields[2])}
              className="cursor-pointer transition-all group"
            >
              <path
                d="M 475 65 L 790 65 Q 820 65 820 100 L 820 420 Q 820 450 780 450 L 475 450 Z"
                fill={activeLayer === 'pest' || activeLayer === 'moisture' ? '#14532d' : 'url(#gnutGrad)'}
                stroke={selectedFieldId === 'field-c' ? '#4ade80' : '#22c55e'}
                strokeWidth={selectedFieldId === 'field-c' ? '4' : '2'}
                className="transition-all hover:opacity-95"
              />
              <text x="520" y="210" fill="#ffffff" fontWeight="bold" fontSize="16" fontFamily="Outfit">
                {language === 'gu' ? 'ખેતર C: મગફળી' : language === 'hi' ? 'खेत C: मूंगफली' : 'Field C: Groundnut GG-20'}
              </text>
              <text x="520" y="235" fill="#bbf7d0" fontSize="13" fontWeight="medium">
                3.2 Acres • {language === 'gu' ? 'સૂયા અવસ્થા' : 'Pod Development'}
              </text>
              <text x="520" y="260" fill="#86efac" fontSize="12">
                {t("common.healthy", "Healthy")} • {t("metrics.farmHealth", "Health")} 92%
              </text>
            </g>

            {/* IoT Central Station */}
            <g transform="translate(435, 245)">
              <circle cx="15" cy="15" r="22" fill="#0284c7" stroke="#38bdf8" strokeWidth="3" className="animate-pulse" />
              <text x="15" y="20" fill="#ffffff" fontSize="12" fontWeight="bold" textAnchor="middle">
                IoT
              </text>
            </g>

            {/* Sensor Pinpoints */}
            {(activeLayer === 'all' || activeLayer === 'sensors') && (
              <>
                <g transform="translate(250, 360)" className="cursor-pointer">
                  <circle cx="0" cy="0" r="10" fill="#eab308" stroke="#ffffff" strokeWidth="2" />
                  <circle cx="0" cy="0" r="18" fill="none" stroke="#eab308" strokeWidth="1.5" className="animate-ping" opacity="0.6" />
                  <text x="14" y="4" fill="#ffffff" fontSize="11" fontWeight="bold">SN-01 (Soil)</text>
                </g>

                <g transform="translate(260, 150)" className="cursor-pointer">
                  <circle cx="0" cy="0" r="10" fill="#ef4444" stroke="#ffffff" strokeWidth="2" />
                  <circle cx="0" cy="0" r="18" fill="none" stroke="#ef4444" strokeWidth="1.5" className="animate-ping" opacity="0.6" />
                  <text x="14" y="4" fill="#ffffff" fontSize="11" fontWeight="bold">SN-02 (Leaf)</text>
                </g>

                <g transform="translate(640, 240)" className="cursor-pointer">
                  <circle cx="0" cy="0" r="10" fill="#22c55e" stroke="#ffffff" strokeWidth="2" />
                  <text x="14" y="4" fill="#ffffff" fontSize="11" fontWeight="bold">SN-03 (Valve)</text>
                </g>
              </>
            )}

            {/* Water flowing animation */}
            {activeValve.fieldA && (
              <g transform="translate(220, 380)">
                <circle cx="0" cy="0" r="28" fill="none" stroke="#38bdf8" strokeWidth="3" className="animate-ping" />
                <text x="0" y="5" fill="#38bdf8" fontSize="10" fontWeight="bold" textAnchor="middle">WATERING</text>
              </g>
            )}

          </svg>
        </div>

        {/* Bottom Legend Overlay */}
        <div className="absolute bottom-4 left-4 z-20 flex flex-wrap items-center gap-3 bg-slate-900/90 backdrop-blur-md px-3.5 py-2 rounded-2xl border border-slate-700 text-xs text-slate-300">
          <span className="font-bold text-white text-[11px] uppercase tracking-wider">Status:</span>
          <span className="flex items-center gap-1.5">
            <span className="w-3 h-3 rounded-full bg-emerald-500"></span>
            {t("common.healthy", "Optimal")}
          </span>
          <span className="flex items-center gap-1.5">
            <span className="w-3 h-3 rounded-full bg-amber-500"></span>
            {t("mapPage.waterStress", "Water Deficit")}
          </span>
          <span className="flex items-center gap-1.5">
            <span className="w-3 h-3 rounded-full bg-rose-500"></span>
            {t("mapPage.pestDanger", "Pest Risk")}
          </span>
        </div>

        {/* Selected Field Quick Inspector Card */}
        {selectedField && (
          <div className="absolute bottom-4 right-4 z-20 bg-white/95 backdrop-blur-md p-4 rounded-2xl shadow-2xl border border-slate-200 w-80 max-w-[calc(100%-2rem)] text-slate-900 animate-in fade-in slide-in-from-bottom-2">
            <div className="flex items-start justify-between">
              <div>
                <span className={`inline-block px-2 py-0.5 rounded-md text-[10px] font-extrabold uppercase ${
                  selectedField.status === 'Critical' ? 'bg-rose-100 text-rose-700' :
                  selectedField.status === 'Warning' ? 'bg-amber-100 text-amber-800' :
                  'bg-emerald-100 text-emerald-800'
                }`}>
                  {selectedField.status}
                </span>
                <h4 className="text-sm font-bold text-slate-900 mt-1">{selectedField.name}</h4>
                <p className="text-xs text-slate-500">{selectedField.crop} • {selectedField.area}</p>
              </div>

              <VoiceSpeaker
                text={`${selectedField.name}. Crop: ${selectedField.crop}. ${selectedField.recommendation}`}
                label={t("common.readAloud", "Listen")}
              />
            </div>

            <div className="grid grid-cols-2 gap-2 mt-3 text-xs bg-slate-50 p-2.5 rounded-xl border border-slate-100">
              <div>
                <span className="text-slate-400 text-[10px] block">{t("metrics.soilMoisture", "Moisture")}</span>
                <span className={`font-bold ${selectedField.soilMoisture < 35 ? 'text-amber-600' : 'text-emerald-600'}`}>
                  {selectedField.soilMoisture}%
                </span>
              </div>
              <div>
                <span className="text-slate-400 text-[10px] block">{t("metrics.farmHealth", "Health")}</span>
                <span className="font-bold text-slate-800">{selectedField.healthScore}%</span>
              </div>
              <div>
                <span className="text-slate-400 text-[10px] block">{t("mapPage.pestDanger", "Pest Risk")}</span>
                <span className="font-semibold text-slate-800 truncate block">{selectedField.pestRisk}</span>
              </div>
              <div>
                <span className="text-slate-400 text-[10px] block">{t("metrics.phLevel", "Soil pH")}</span>
                <span className="font-semibold text-slate-800">{selectedField.soilPH}</span>
              </div>
            </div>

            <div className="mt-3 flex items-center gap-2">
              {selectedField.id === 'field-a' ? (
                <button
                  onClick={() => triggerIrrigationValve('field-a', 35)}
                  className="flex-1 py-2 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-600 text-white text-xs font-bold hover:shadow-md hover:shadow-emerald-500/20 transition-all flex items-center justify-center gap-1.5"
                >
                  <Droplets className="w-3.5 h-3.5" />
                  <span>{t("mapPage.triggerDrip", "Quick Drip Water (35m)")}</span>
                </button>
              ) : (
                <button
                  onClick={() => setSelectedFieldId(selectedField.id)}
                  className="flex-1 py-2 rounded-xl bg-slate-900 text-white text-xs font-bold hover:bg-slate-800 transition-all"
                >
                  {t("mapPage.inspectZone", "Inspect Details")}
                </button>
              )}
            </div>
          </div>
        )}

      </div>
    </div>
  );
}
