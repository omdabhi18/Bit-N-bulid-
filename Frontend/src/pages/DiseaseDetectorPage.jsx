import React, { useState, useEffect, useRef } from 'react';
import { useLanguage } from '../context/LanguageContext';
import { useFarm } from '../context/FarmContext';
import VoiceSpeaker from '../components/common/VoiceSpeaker';
import {
  ScanEye,
  Camera,
  Sparkles,
  ShieldAlert,
  Sprout,
  HelpCircle,
  ArrowRight,
  Search,
  AlertTriangle,
  Database,
  CheckCircle2,
  Clock
} from 'lucide-react';
import { cropDiseaseCatalog } from '../data/mockFarmData';
import { Link } from 'react-router-dom';

const CATEGORIES = ['All', 'Cash Crop', 'Cereal', 'Vegetable', 'Oilseed', 'Pulse', 'Millet'];

export default function DiseaseDetectorPage() {
  const { t, language } = useLanguage();
  const fileInputRef = useRef(null);

  const [cropsCatalog, setCropsCatalog] = useState([]);
  const [selectedCrop, setSelectedCrop] = useState(null);
  const [selectedDisease, setSelectedDisease] = useState(cropDiseaseCatalog[0]);
  const [isScanning, setIsScanning] = useState(false);
  const [scanComplete, setScanComplete] = useState(true);
  const [isUnsupported, setIsUnsupported] = useState(false);
  const [unsupportedMessage, setUnsupportedMessage] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [loadingCrops, setLoadingCrops] = useState(true);

  // Fetch crops catalog from backend database
  useEffect(() => {
    let isMounted = true;
    fetch('/api/crops')
      .then(res => res.json())
      .then(data => {
        if (isMounted && data?.crops) {
          setCropsCatalog(data.crops);
          const defaultCrop = data.crops.find(c => c.id === 'cotton') || data.crops[0];
          setSelectedCrop(defaultCrop);
        }
      })
      .catch(err => console.error("Error loading crops catalog:", err))
      .finally(() => {
        if (isMounted) setLoadingCrops(false);
      });
    return () => { isMounted = false; };
  }, []);

  // Handle selecting any crop from the DB catalog
  const handleSelectCrop = async (crop) => {
    setSelectedCrop(crop);
    setIsScanning(true);
    setScanComplete(false);

    if (!crop.disease_ai_supported) {
      // Crop not supported by AI: Do not generate fake predictions
      setIsScanning(false);
      setScanComplete(true);
      setIsUnsupported(true);
      setUnsupportedMessage(
        language === 'gu'
          ? 'આ પાક માટે AI રોગ તપાસ હાલમાં ઉપલબ્ધ નથી. તમે કૃષિ નિષ્ણાતની સમીક્ષા માટે વિનંતી કરી શકો છો.'
          : 'AI analysis is currently unavailable for this crop. You can request expert review.'
      );
      setSelectedDisease({
        id: `unsupp-${crop.id}`,
        crop: language === 'gu' && crop.name_gujarati ? `${crop.name} (${crop.name_gujarati})` : crop.name,
        diseaseName: 'AI Analysis Unavailable',
        diseaseNameGu: 'આ પાક માટે AI રોગ તપાસ ઉપલબ્ધ નથી',
        confidence: 0,
        severity: 'Low',
        image: 'https://images.unsplash.com/photo-1592417817098-8f3d6910985b?auto=format&fit=crop&w=800&q=80',
        symptoms: [
          language === 'gu'
            ? 'આ પાકની જાત માટે AI વિઝન રોગ તપાસ મોડેલ હાલ ઉપલબ્ધ નથી.'
            : 'AI disease vision model is not yet verified for this crop variety.'
        ],
        recommendedRemedy: {
          organic: language === 'gu'
            ? 'કૃપા કરીને યુનિવર્સિટી કૃષિ વૈજ્ઞાનિકને પાંદડાનો ફોટો મોકલી વિનંતી કરો.'
            : 'Please submit a leaf photo to our university agronomists for manual lab inspection.',
          chemical: language === 'gu'
            ? 'નિષ્ણાતની સલાહ વગર કોઈ રાસાયણિક દવાનો છંટકાવ ન કરો.'
            : 'Do not spray arbitrary chemicals without an agronomist prescription.',
          prevention: language === 'gu'
            ? 'નિયમિત ખેતર નિરીક્ષણ કરો અને યોગ્ય અંતર જાળવો.'
            : 'Regular scouting and proper spacing until expert advisory is received.'
        }
      });
      return;
    }

    // Supported crop: query API for analysis & persistence
    setIsUnsupported(false);
    setUnsupportedMessage('');

    try {
      const res = await fetch('/api/disease/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({ cropId: crop.id })
      });
      const data = await res.json();
      if (data && data.supported) {
        setSelectedDisease({
          id: data.id,
          crop: data.crop,
          diseaseName: data.diseaseName,
          diseaseNameGu: data.diseaseNameGu,
          confidence: data.confidence,
          severity: data.severity,
          image: data.imageUrl,
          symptoms: data.symptoms,
          recommendedRemedy: data.recommendedRemedy
        });
      }
    } catch (err) {
      console.error("Analysis error:", err);
    } finally {
      setIsScanning(false);
      setScanComplete(true);
    }
  };

  // Handle selecting one of the 4 original field test samples (demo mode)
  const handleSelectSample = async (item) => {
    setIsScanning(true);
    setScanComplete(false);
    setIsUnsupported(false);
    setUnsupportedMessage('');

    const matchedCrop = cropsCatalog.find(
      c => c.id === item.id || c.name.toLowerCase() === item.crop.toLowerCase().split(' ')[0]
    );
    if (matchedCrop) {
      setSelectedCrop(matchedCrop);
    }

    try {
      const res = await fetch('/api/disease/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({ sampleId: item.id })
      });
      const data = await res.json();
      if (data && data.supported) {
        setSelectedDisease({
          id: data.id,
          crop: data.crop,
          diseaseName: data.diseaseName,
          diseaseNameGu: data.diseaseNameGu,
          confidence: data.confidence,
          severity: data.severity,
          image: data.imageUrl,
          symptoms: data.symptoms,
          recommendedRemedy: data.recommendedRemedy
        });
      } else {
        setSelectedDisease(item);
      }
    } catch (e) {
      setSelectedDisease(item);
    } finally {
      setIsScanning(false);
      setScanComplete(true);
    }
  };

  // Handle image upload from farmer's device
  const handleFileUpload = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setIsScanning(true);
    setScanComplete(false);

    const formData = new FormData();
    formData.append('file', file);
    if (selectedCrop) {
      formData.append('cropId', selectedCrop.id);
    }

    try {
      const res = await fetch('/api/disease/analyze', {
        method: 'POST',
        body: formData
      });
      const data = await res.json();
      if (data) {
        if (!data.supported) {
          setIsUnsupported(true);
          setUnsupportedMessage(
            data.message || (language === 'gu'
              ? 'આ પાક માટે AI રોગ તપાસ હાલમાં ઉપલબ્ધ નથી. તમે કૃષિ નિષ્ણાતની સમીક્ષા માટે વિનંતી કરી શકો છો.'
              : 'AI analysis is currently unavailable for this crop. You can request expert review.')
          );
        } else {
          setIsUnsupported(false);
          setUnsupportedMessage('');
        }
        setSelectedDisease({
          id: data.id,
          crop: data.crop,
          diseaseName: data.diseaseName,
          diseaseNameGu: data.diseaseNameGu,
          confidence: data.confidence,
          severity: data.severity,
          image: data.imageUrl,
          symptoms: data.symptoms,
          recommendedRemedy: data.recommendedRemedy
        });
      }
    } catch (err) {
      console.error("Upload error:", err);
    } finally {
      setIsScanning(false);
      setScanComplete(true);
    }
  };

  // Filter crops based on search term (English & Gujarati) and category
  const filteredCrops = cropsCatalog.filter(crop => {
    const query = searchQuery.trim().toLowerCase();
    const matchesSearch = !query ||
      crop.name.toLowerCase().includes(query) ||
      (crop.name_gujarati && crop.name_gujarati.toLowerCase().includes(query));
    
    const matchesCategory = selectedCategory === 'All' ||
      (crop.category && crop.category.toLowerCase().includes(selectedCategory.toLowerCase()));

    return matchesSearch && matchesCategory;
  });

  const diseaseTitle = language === 'gu' && selectedDisease.diseaseNameGu
    ? selectedDisease.diseaseNameGu
    : selectedDisease.diseaseName;

  const audioText = isUnsupported
    ? (language === 'gu'
        ? 'આ પાક માટે AI રોગ તપાસ હાલમાં ઉપલબ્ધ નથી. કૃપા કરીને યુનિવર્સિટી કૃષિ નિષ્ણાતની સમીક્ષા માટે વિનંતી કરો.'
        : 'AI analysis is currently unavailable for this crop. Please request expert review.')
    : (language === 'gu'
        ? `પાક રોગ તપાસ. અત્યારે ${diseaseTitle} ની તપાસ થયેલ છે. AI ચોકસાઈ ${selectedDisease.confidence} ટકા છે.`
        : `Crop disease detection page. Currently inspecting ${diseaseTitle}. AI confidence is ${selectedDisease.confidence} percent.`);

  return (
    <div className="space-y-6">
      
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-white p-5 rounded-3xl border border-slate-200 shadow-card-soft">
        <div>
          <div className="flex items-center gap-2">
            <span className="p-2 rounded-xl bg-rose-100 text-rose-800">
              <ScanEye className="w-5 h-5" />
            </span>
            <div>
              <h1 className="text-xl sm:text-2xl font-extrabold text-slate-900 tracking-tight">
                {t("diseasePage.title", "AI Vision Crop Disease & Pest Detector")}
              </h1>
              <p className="text-xs text-slate-500">
                {t("diseasePage.subtitle", "Upload leaf photo from the field for instant computer-vision pathogen detection and organic treatment")}
              </p>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <VoiceSpeaker
            text={audioText}
            label={t("diseasePage.listenDiagnosis", "Listen Diagnosis")}
          />
        </div>
      </div>

      {/* Upload Zone & Sample Selector */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* Left 5 Cols: Visual Scanner, Database Crop Catalog & 4 Demo Samples */}
        <div className="lg:col-span-5 space-y-4">
          
          <div className="bg-white p-5 rounded-3xl border border-slate-200 shadow-card-soft space-y-4">
            
            <div className="flex items-center justify-between">
              <h3 className="font-bold text-slate-900 text-sm flex items-center gap-2">
                <Camera className="w-4 h-4 text-emerald-600" />
                {t("diseasePage.captureUpload", "Capture or Upload Leaf Image")}
              </h3>
              <button
                onClick={() => fileInputRef.current?.click()}
                className="text-xs font-semibold px-2.5 py-1 rounded-lg bg-emerald-50 text-emerald-700 hover:bg-emerald-100 border border-emerald-200 transition-colors"
              >
                {language === 'gu' ? 'ફોટો પસંદ કરો' : 'Choose File'}
              </button>
              <input
                ref={fileInputRef}
                type="file"
                accept="image/*"
                className="hidden"
                onChange={handleFileUpload}
              />
            </div>

            {/* Camera Viewfinder */}
            <div className="relative aspect-[4/3] rounded-2xl overflow-hidden bg-slate-950 border-2 border-slate-700 shadow-inner group">
              <img
                src={selectedDisease.image}
                alt={selectedDisease.diseaseName}
                className={`w-full h-full object-cover transition-opacity duration-300 ${isScanning ? 'opacity-40' : 'opacity-90'}`}
              />

              {isScanning && (
                <div className="absolute inset-x-0 h-1 bg-gradient-to-r from-emerald-400 via-teal-300 to-emerald-500 shadow-glow-green animate-bounce" />
              )}

              {scanComplete && !isScanning && !isUnsupported && (
                <div className="absolute top-1/4 left-1/4 w-1/2 h-1/2 border-2 border-dashed border-rose-400 rounded-xl bg-rose-500/10 pointer-events-none animate-pulse">
                  <span className="absolute -top-3 left-2 bg-rose-600 text-white text-[9px] font-bold px-1.5 py-0.5 rounded shadow">
                    Pathogen Signature ({selectedDisease.confidence}%)
                  </span>
                </div>
              )}

              {scanComplete && !isScanning && isUnsupported && (
                <div className="absolute top-1/4 left-1/4 w-1/2 h-1/2 border-2 border-dashed border-amber-400 rounded-xl bg-amber-500/10 pointer-events-none flex items-center justify-center">
                  <span className="bg-amber-600 text-white text-[10px] font-bold px-2 py-1 rounded shadow flex items-center gap-1">
                    <AlertTriangle className="w-3 h-3" />
                    {language === 'gu' ? 'AI અસમર્થિત' : 'AI Unsupported'}
                  </span>
                </div>
              )}

              <div className="absolute bottom-3 left-3 right-3 bg-slate-900/80 backdrop-blur-md p-2.5 rounded-xl text-white text-xs flex items-center justify-between">
                <span className="flex items-center gap-1.5 text-[11px] font-semibold">
                  <Sparkles className="w-3.5 h-3.5 text-emerald-400" />
                  {isScanning
                    ? (language === 'gu' ? "વિઝન એજન્ટ સ્કેનિંગ..." : "Scanning with Vision Agent...")
                    : (isUnsupported ? (language === 'gu' ? "લેબ સમીક્ષા જરૂરી" : "Lab Review Required") : (language === 'gu' ? "ચકાસણી પૂર્ણ" : "Analysis Complete"))}
                </span>
                <span className="text-emerald-400 font-bold truncate max-w-[150px]">
                  {selectedCrop ? `${selectedCrop.name}${selectedCrop.name_gujarati ? ` (${selectedCrop.name_gujarati})` : ''}` : selectedDisease.crop}
                </span>
              </div>
            </div>

            {/* Database Crop Catalog Selector */}
            <div className="space-y-2 pt-1 border-t border-slate-100">
              <div className="flex items-center justify-between">
                <span className="text-[11px] font-bold text-slate-500 uppercase tracking-wider flex items-center gap-1.5">
                  <Database className="w-3.5 h-3.5 text-emerald-600" />
                  {t("diseasePage.selectCropCatalog", "Select Crop from Database Catalog:")}
                </span>
                <span className="text-[10px] font-semibold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-full">
                  {cropsCatalog.length} {language === 'gu' ? 'પાક' : 'Crops'}
                </span>
              </div>

              {/* Search Bar */}
              <div className="relative">
                <Search className="w-3.5 h-3.5 text-slate-400 absolute left-2.5 top-1/2 -translate-y-1/2" />
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder={t("diseasePage.searchCrops", "Search crop in English or ગુજરાતી...")}
                  className="w-full pl-8 pr-3 py-1.5 text-xs rounded-xl border border-slate-200 focus:outline-none focus:border-emerald-500 bg-slate-50/50"
                />
              </div>

              {/* Category Filter Pills */}
              <div className="flex gap-1 overflow-x-auto pb-1 no-scrollbar text-[10px]">
                {CATEGORIES.map(cat => (
                  <button
                    key={cat}
                    onClick={() => setSelectedCategory(cat)}
                    className={`px-2 py-0.5 rounded-lg whitespace-nowrap transition-colors ${
                      selectedCategory === cat
                        ? 'bg-slate-900 text-white font-bold'
                        : 'bg-slate-100 hover:bg-slate-200 text-slate-600'
                    }`}
                  >
                    {cat === 'All' ? t("diseasePage.allCategories", "All") : cat}
                  </button>
                ))}
              </div>

              {/* Scrollable Crop List from DB */}
              <div className="max-h-40 overflow-y-auto space-y-1 pr-1 border border-slate-100 rounded-xl p-1.5 bg-slate-50/30">
                {loadingCrops ? (
                  <div className="text-center py-4 text-xs text-slate-400">Loading crops...</div>
                ) : filteredCrops.length === 0 ? (
                  <div className="text-center py-4 text-xs text-slate-400">No crops match query</div>
                ) : (
                  filteredCrops.map(crop => {
                    const isSelected = selectedCrop?.id === crop.id;
                    return (
                      <button
                        key={crop.id}
                        onClick={() => handleSelectCrop(crop)}
                        className={`w-full p-2 rounded-xl text-left border transition-all text-xs flex items-center justify-between gap-2 ${
                          isSelected
                            ? 'border-emerald-500 bg-emerald-50 text-emerald-950 font-bold shadow-sm'
                            : 'border-slate-200/80 hover:border-slate-300 bg-white text-slate-700'
                        }`}
                      >
                        <div className="flex items-center gap-2 truncate">
                          <span className={`w-2 h-2 rounded-full shrink-0 ${crop.disease_ai_supported ? 'bg-emerald-500' : 'bg-amber-500'}`} />
                          <span className="truncate">
                            {crop.name} {crop.name_gujarati && <span className="text-slate-500 font-normal">({crop.name_gujarati})</span>}
                          </span>
                        </div>

                        <span className={`text-[9px] font-bold px-1.5 py-0.5 rounded shrink-0 uppercase tracking-wide ${
                          crop.disease_ai_supported
                            ? 'bg-emerald-100 text-emerald-800'
                            : 'bg-amber-100 text-amber-800'
                        }`}>
                          {crop.disease_ai_supported ? t("diseasePage.aiSupported", "AI Ready") : t("diseasePage.labReviewOnly", "Lab Review")}
                        </span>
                      </button>
                    );
                  })
                )}
              </div>
            </div>

            {/* 4 Realistic Field Test Samples (Preserved Demo Options) */}
            <div className="pt-2 border-t border-slate-100">
              <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider block mb-2">
                {t("diseasePage.selectSamples", "Or Select Realistic Field Test Samples:")}
              </span>
              <div className="grid grid-cols-2 gap-2">
                {cropDiseaseCatalog.map((item) => (
                  <button
                    key={item.id}
                    onClick={() => handleSelectSample(item)}
                    className={`p-2 rounded-xl text-left border transition-all text-xs flex items-center gap-2 ${
                      selectedDisease.id === item.id && !isUnsupported
                        ? 'border-emerald-500 bg-emerald-50 text-emerald-900 font-bold shadow-sm'
                        : 'border-slate-200 hover:border-slate-300 bg-white text-slate-600'
                    }`}
                  >
                    <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
                    <span className="truncate">{item.crop}</span>
                  </button>
                ))}
              </div>
            </div>

          </div>

        </div>

        {/* Right 7 Cols: Diagnosis & Treatment Blueprint */}
        <div className="lg:col-span-7 space-y-4">
          
          <div className="bg-white p-6 rounded-3xl border border-slate-200/80 shadow-card-soft space-y-4">
            
            {/* If Crop is Unsupported: Show clear warning banner and agronomist escalation action */}
            {isUnsupported ? (
              <div className="space-y-4">
                <div className="p-5 rounded-2xl bg-amber-50 border-2 border-amber-300 text-amber-950 space-y-3">
                  <div className="flex items-center gap-2 font-extrabold text-sm text-amber-900">
                    <AlertTriangle className="w-5 h-5 text-amber-600 shrink-0" />
                    <span>{t("diseasePage.aiUnavailableTitle", "AI Analysis Unavailable")}</span>
                  </div>
                  <p className="text-xs text-amber-900 font-medium leading-relaxed">
                    {unsupportedMessage || t("diseasePage.unsupportedWarning", "AI analysis is currently unavailable for this crop. You can request expert review.")}
                  </p>
                  <div className="pt-1">
                    <Link
                      to={`/escalation?crop=${encodeURIComponent(selectedCrop ? selectedCrop.name : 'Crop')}`}
                      className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-amber-600 hover:bg-amber-700 text-white text-xs font-bold transition-all shadow"
                    >
                      <span>{t("diseasePage.requestExpertReview", "Request Agronomist Lab Review")}</span>
                      <ArrowRight className="w-3.5 h-3.5" />
                    </Link>
                  </div>
                </div>

                <div className="space-y-2 bg-slate-50 p-4 rounded-2xl border border-slate-200 text-xs text-slate-700 space-y-2">
                  <span className="font-bold text-slate-900 uppercase tracking-wider block">
                    {language === 'gu' ? 'કૃષિ વિજ્ઞાન માર્ગદર્શન:' : 'Field Scouting Protocols:'}
                  </span>
                  <div className="flex items-start gap-2">
                    <span className="text-emerald-600 font-bold">•</span>
                    <span>
                      {language === 'gu'
                        ? 'આ પાક (જેમ કે બાજરી, જુવાર, કોબી, શેરડી) માટે સ્વચાલિત વિઝન મોડેલ પૂર્વાવલોકન હેઠળ છે.'
                        : `Automated vision diagnostics for ${selectedCrop ? selectedCrop.name : 'this crop'} is currently undergoing university agronomist calibration.`}
                    </span>
                  </div>
                  <div className="flex items-start gap-2">
                    <span className="text-rose-500 font-bold">•</span>
                    <span>
                      {language === 'gu'
                        ? 'કોઈપણ અપ્રમાણિત રાસાયણિક કીટનાશકનો છંટકાવ કરવો નહીં.'
                        : 'Do NOT apply unprescribed chemical interventions without verified agronomist confirmation.'}
                    </span>
                  </div>
                  <div className="flex items-start gap-2">
                    <span className="text-sky-500 font-bold">•</span>
                    <span>
                      {language === 'gu'
                        ? 'નજીકના APMC અથવા કૃષિ વિજ્ઞાન કેન્દ્ર (KVK) નો સંપર્ક કરી શકો છો.'
                        : 'You can directly escalate this specimen to university scientists using the ticket button below.'}
                    </span>
                  </div>
                </div>
              </div>
            ) : (
              /* If Crop is Supported: Show Full Diagnosis & Agronomic Treatment */
              <>
                <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-3 pb-3 border-b border-slate-100">
                  <div>
                    <span className={`inline-block px-2.5 py-0.5 rounded-full text-[10px] font-extrabold uppercase ${
                      selectedDisease.severity === 'Critical' ? 'bg-rose-100 text-rose-800' :
                      selectedDisease.severity === 'High' ? 'bg-amber-100 text-amber-800' :
                      'bg-sky-100 text-sky-800'
                    }`}>
                      {selectedDisease.severity} {t("common.priority", "Severity")}
                    </span>
                    <h2 className="text-xl font-extrabold text-slate-900 mt-1">{diseaseTitle}</h2>
                    <p className="text-xs text-slate-500">{selectedDisease.crop}</p>
                  </div>

                  <div className="text-right shrink-0">
                    <span className="text-2xl font-extrabold text-emerald-700">{selectedDisease.confidence}%</span>
                    <span className="text-[10px] text-slate-400 font-semibold block">{t("common.confidence", "Vision Confidence")}</span>
                  </div>
                </div>

                <div className="space-y-2">
                  <span className="text-xs font-bold text-slate-700 uppercase tracking-wider block">
                    {t("diseasePage.visualSymptoms", "Visual Symptoms Detected:")}
                  </span>
                  <div className="space-y-1.5 bg-slate-50 p-3 rounded-2xl border border-slate-100 text-xs">
                    {selectedDisease.symptoms.map((sym, idx) => (
                      <div key={idx} className="flex items-start gap-2 text-slate-700">
                        <span className="text-rose-500 font-bold">•</span>
                        <span>{sym}</span>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="space-y-3 pt-2">
                  <h3 className="text-xs font-bold text-slate-800 uppercase tracking-wider">
                    {t("diseasePage.treatmentGuidelines", "Agronomic Treatment Guidelines:")}
                  </h3>

                  <div className="p-4 rounded-2xl bg-emerald-50/80 border border-emerald-200 text-xs space-y-1">
                    <div className="flex items-center gap-1.5 text-emerald-900 font-bold">
                      <Sprout className="w-4 h-4 text-emerald-600" />
                      <span>{t("diseasePage.organicRemedy", "Organic / Bio-Control Remedy:")}</span>
                    </div>
                    <p className="text-emerald-800 pl-5 leading-relaxed">
                      {selectedDisease.recommendedRemedy.organic}
                    </p>
                  </div>

                  <div className="p-4 rounded-2xl bg-amber-50/80 border border-amber-200 text-xs space-y-1">
                    <div className="flex items-center gap-1.5 text-amber-900 font-bold">
                      <ShieldAlert className="w-4 h-4 text-amber-600" />
                      <span>{t("diseasePage.chemicalIntervention", "Chemical Intervention:")}</span>
                    </div>
                    <p className="text-amber-800 pl-5 leading-relaxed">
                      {selectedDisease.recommendedRemedy.chemical}
                    </p>
                  </div>

                  <div className="p-3.5 rounded-2xl bg-slate-50 border border-slate-200 text-xs text-slate-600">
                    <span className="font-bold text-slate-800 block mb-0.5">{t("diseasePage.preventiveAdvice", "Preventive Advice:")}</span>
                    {selectedDisease.recommendedRemedy.prevention}
                  </div>
                </div>
              </>
            )}

            <div className="pt-3 border-t border-slate-100 flex flex-wrap items-center justify-between gap-3">
              <span className="text-xs text-slate-500 flex items-center gap-1">
                <HelpCircle className="w-3.5 h-3.5 text-slate-400" />
                {t("diseasePage.unsureDiag", "Unsure about diagnosis?")}
              </span>

              <Link
                to={`/escalation?crop=${encodeURIComponent(selectedCrop ? selectedCrop.name : 'General')}`}
                className="px-4 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 text-white text-xs font-bold flex items-center gap-1.5 transition-all shadow"
              >
                <span>{t("diseasePage.escalateAgronomist", "Escalate to University Agronomist")}</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </Link>
            </div>

          </div>

        </div>

      </div>

    </div>
  );
}
