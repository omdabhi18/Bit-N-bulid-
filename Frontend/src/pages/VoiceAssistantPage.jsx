import React, { useState, useRef, useEffect } from 'react';
import { useLanguage } from '../context/LanguageContext';
import { useFarm } from '../context/FarmContext';
import {
  Mic,
  MicOff,
  Send,
  Bot,
  Volume2,
  Droplets
} from 'lucide-react';

export default function VoiceAssistantPage() {
  const { language, setLanguage, speak, t } = useLanguage();
  const { triggerIrrigationValve } = useFarm();
  const [messages, setMessages] = useState([
    {
      id: 1,
      sender: 'ai',
      text: language === 'gu'
        ? "નમસ્તે કિશનભાઈ! હું તમારો કિસાન AI સહાયક છું. તમારા ખેતરના ભેજ, હવામાન, જીવાત કે બજાર ભાવ વિશે મને ગુજરાતીમાં પૂછી શકો છો."
        : language === 'hi'
        ? "नमस्ते किशनभाई! मैं आपका किसान AI सहायक हूँ। अपने खेत की नमी, मौसम, कीट या मंडी भाव के बारे में मुझसे पूछें।"
        : "Hello Kishanbhai! I am your Kisan AI assistant. You can ask me about soil moisture, weather forecast, pest risks, or APMC mandi rates.",
      time: "Just now",
      suggestions: [
        language === 'gu' ? "મારા કપાસમાં આજે પાણી આપવું જોઈએ?" : "Should I irrigate Field A today?",
        language === 'gu' ? "આજે ગોંડલ માર્કેટમાં કપાસનો ભાવ શું છે?" : "What is today's cotton rate in Gondal APMC?",
        language === 'gu' ? "ખેતર B માં ફોસ્ફરસ કેમ ઓછું છે?" : "Why is phosphorus low in Field B?"
      ]
    }
  ]);
  const [inputQuery, setInputQuery] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = (textToSend) => {
    const query = textToSend || inputQuery;
    if (!query.trim()) return;

    const userMsg = {
      id: Date.now(),
      sender: 'user',
      text: query,
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setMessages(prev => [...prev, userMsg]);
    setInputQuery('');

    setTimeout(() => {
      let aiResponseText = "";
      let actionRecommendation = null;

      const q = query.toLowerCase();
      if (q.includes('pani') || q.includes('water') || q.includes('irrigate') || q.includes('સિંચાઈ') || q.includes('પાણી')) {
        aiResponseText = language === 'gu'
          ? `Field A (કપાસ) માં જમીનનો ભેજ અત્યારે ૩૧% છે. આગામી ૨૪ કલાકમાં વરસાદની શક્યતા માત્ર ૧૨% છે. તેથી આજે સાંજે ૬:૦૦ વાગ્યે ૩૫ મિનિટ માટે ડ્રિપ પિયત આપવાની ભલામણ છે.`
          : language === 'hi'
          ? `खेत A (कपास) में मिट्टी की नमी वर्तमान में 31% है। अगले 24 घंटों में बारिश की संभावना केवल 12% है। इसलिए आज शाम 6:00 बजे ड्रिप सिंचाई करना आवश्यक है।`
          : `Field A (Cotton) root moisture is at 31.4% with only 12% rainfall probability. Drip irrigation for 35 minutes (2,500 L) is recommended today at 18:00 IST.`;
        actionRecommendation = "irrigate";
      } else if (q.includes('bhav') || q.includes('rate') || q.includes('price') || q.includes('મંડી') || q.includes('ભાવ')) {
        aiResponseText = language === 'gu'
          ? `આજે ગોંડલ માર્કેટ યાર્ડમાં શંકર-૬ કપાસનો ભાવ ₹૭,૪૨૦ પ્રતિ ક્વિન્ટલ છે (રાજકોટ કરતાં ₹૪૦ વધારે). આગામી ૪ થી ૬ દિવસમાં માલ વેચવા માટે ઉત્તમ સમય છે.`
          : `Today's Shankar-6 Cotton rate in Gondal APMC is ₹7,420/quintal (₹40 higher than Rajkot). AI recommends selling within the next 4-6 days.`;
      } else if (q.includes('phosphorus') || q.includes('ખાતર') || q.includes('fertilizer') || q.includes('ફોસ્ફરસ')) {
        aiResponseText = language === 'gu'
          ? `ખેતર B (ઘઉં) માં ઉપલબ્ધ ફોસ્ફરસ ૧૪ mg/kg છે, જે સામાન્ય કરતાં ઓછું છે. આવતીકાલે સવારે ૧૫ કિલો વોટર સોલ્યુબલ DAP ખાતર ડ્રિપ દ્વારા આપવું.`
          : `Phosphorus is at 14 mg/kg in Field B due to rapid tillering uptake. Apply 15 kg water-soluble DAP during tomorrow's fertigation cycle.`;
      } else {
        aiResponseText = language === 'gu'
          ? `કિશનભાઈ, તમારા ખેતરનું સમગ્ર સ્વાસ્થ્ય ૮૨% છે. બધા સેન્સર ઓનલાઇન છે. ખેતર A માં પિયત આપવું સૌથી તાત્કાલિક કામ છે.`
          : `Kishanbhai, overall farm health index is 82%. All 4 IoT nodes are active. The most immediate priority is executing irrigation in Field A.`;
      }

      const aiMsg = {
        id: Date.now() + 1,
        sender: 'ai',
        text: aiResponseText,
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        actionRecommendation
      };

      setMessages(prev => [...prev, aiMsg]);
      speak(aiResponseText);
    }, 800);
  };

  const toggleMic = () => {
    if (isRecording) {
      setIsRecording(false);
      handleSend(language === 'gu' ? "મારા કપાસમાં આજે પાણી આપવું જોઈએ?" : "Should I irrigate Field A today?");
    } else {
      setIsRecording(true);
      setTimeout(() => {
        setIsRecording(false);
        handleSend(language === 'gu' ? "મારા કપાસમાં આજે પાણી આપવું જોઈએ?" : "Should I irrigate Field A today?");
      }, 2500);
    }
  };

  return (
    <div className="space-y-6">
      
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-white p-5 rounded-3xl border border-slate-200 shadow-card-soft">
        <div>
          <div className="flex items-center gap-2">
            <span className="p-2 rounded-xl bg-gradient-to-r from-emerald-500 to-teal-600 text-white">
              <Mic className="w-5 h-5" />
            </span>
            <div>
              <h1 className="text-xl sm:text-2xl font-extrabold text-slate-900 tracking-tight">
                {t("assistantPage.title", "Kisan AI Vernacular Voice & Chat Assistant")}
              </h1>
              <p className="text-xs text-slate-500">
                {t("assistantPage.subtitle", "Talk directly in Gujarati, Hindi, or English for immediate farm intelligence")}
              </p>
            </div>
          </div>
        </div>

        {/* Language Pill Switcher */}
        <div className="flex items-center bg-slate-100 p-1 rounded-2xl border border-slate-200 text-xs font-bold">
          <button
            onClick={() => setLanguage('gu')}
            className={`px-3 py-1.5 rounded-xl transition-all ${
              language === 'gu' ? 'bg-white text-emerald-800 shadow-sm font-bold' : 'text-slate-600'
            }`}
          >
            ગુજરાતી
          </button>
          <button
            onClick={() => setLanguage('hi')}
            className={`px-3 py-1.5 rounded-xl transition-all ${
              language === 'hi' ? 'bg-white text-emerald-800 shadow-sm font-bold' : 'text-slate-600'
            }`}
          >
            हिंदी
          </button>
          <button
            onClick={() => setLanguage('en')}
            className={`px-3 py-1.5 rounded-xl transition-all ${
              language === 'en' ? 'bg-white text-emerald-800 shadow-sm font-bold' : 'text-slate-600'
            }`}
          >
            English
          </button>
        </div>
      </div>

      {/* Main Chat & Voice Interface */}
      <div className="bg-white rounded-3xl border border-slate-200 shadow-card-soft h-[540px] flex flex-col overflow-hidden">
        
        <div className="flex-1 p-5 overflow-y-auto space-y-4">
          {messages.map((m) => (
            <div
              key={m.id}
              className={`flex gap-3 ${m.sender === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              {m.sender === 'ai' && (
                <div className="w-9 h-9 rounded-2xl bg-gradient-to-tr from-emerald-600 to-teal-500 text-white flex items-center justify-center shrink-0 shadow-md">
                  <Bot className="w-5 h-5" />
                </div>
              )}

              <div
                className={`max-w-xl p-4 rounded-3xl text-xs sm:text-sm leading-relaxed space-y-2 shadow-sm ${
                  m.sender === 'user'
                    ? 'bg-slate-900 text-white rounded-br-none'
                    : 'bg-slate-50 text-slate-800 border border-slate-200/80 rounded-bl-none'
                }`}
              >
                <div className="flex items-center justify-between gap-4">
                  <span className="font-bold text-[11px] text-slate-400">
                    {m.sender === 'user' ? 'Kishan Patel' : 'Kisan AI Brain'}
                  </span>
                  <div className="flex items-center gap-1.5">
                    <span className="text-[10px] text-slate-400">{m.time}</span>
                    {m.sender === 'ai' && (
                      <button
                        onClick={() => speak(m.text)}
                        className="p-1 rounded text-emerald-600 hover:bg-emerald-50"
                        title={t("common.readAloud", "Listen")}
                      >
                        <Volume2 className="w-3.5 h-3.5" />
                      </button>
                    )}
                  </div>
                </div>

                <p className="font-medium">{m.text}</p>

                {m.actionRecommendation === 'irrigate' && (
                  <div className="pt-2 border-t border-slate-200/60 flex items-center gap-2">
                    <button
                      onClick={() => triggerIrrigationValve('field-a', 35)}
                      className="px-3.5 py-1.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs flex items-center gap-1.5 shadow-sm transition-all"
                    >
                      <Droplets className="w-3.5 h-3.5" />
                      <span>{t("dashboard.openValveNow", "Execute Drip Irrigation Now (Field A)")}</span>
                    </button>
                  </div>
                )}

                {m.suggestions && (
                  <div className="pt-2 border-t border-slate-200/60 space-y-1.5">
                    <span className="text-[10px] text-slate-400 font-bold uppercase tracking-wider block">
                      {t("assistantPage.quickQuestions", "Quick Questions to Ask:")}
                    </span>
                    <div className="flex flex-wrap gap-1.5">
                      {m.suggestions.map((sug, i) => (
                        <button
                          key={i}
                          onClick={() => handleSend(sug)}
                          className="px-2.5 py-1 rounded-xl bg-white border border-slate-200 hover:border-emerald-500 hover:text-emerald-700 text-slate-600 text-[11px] font-medium transition-all text-left"
                        >
                          {sug}
                        </button>
                      ))}
                    </div>
                  </div>
                )}
              </div>

              {m.sender === 'user' && (
                <div className="w-9 h-9 rounded-2xl bg-amber-100 border border-amber-300 text-amber-800 font-bold text-xs flex items-center justify-center shrink-0">
                  KP
                </div>
              )}
            </div>
          ))}
          <div ref={chatEndRef} />
        </div>

        {/* Input Tray */}
        <div className="p-4 bg-slate-50 border-t border-slate-200 space-y-3">
          {isRecording && (
            <div className="flex items-center justify-center gap-2 py-1.5 px-4 rounded-2xl bg-rose-50 border border-rose-200 text-rose-700 text-xs font-bold animate-pulse">
              <span className="w-2.5 h-2.5 rounded-full bg-rose-500 animate-ping"></span>
              <span>{t("assistantPage.listening", "Listening to your voice... Speak now!")}</span>
            </div>
          )}

          <div className="flex items-center gap-2">
            <button
              onClick={toggleMic}
              className={`p-3 rounded-2xl transition-all shadow-md ${
                isRecording
                  ? 'bg-rose-600 text-white animate-bounce'
                  : 'bg-gradient-to-r from-emerald-600 to-teal-600 text-white hover:scale-105'
              }`}
              title={isRecording ? "Stop voice input" : "Speak to Kisan AI"}
            >
              {isRecording ? <MicOff className="w-5 h-5" /> : <Mic className="w-5 h-5" />}
            </button>

            <input
              type="text"
              value={inputQuery}
              onChange={(e) => setInputQuery(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSend()}
              placeholder={t("assistantPage.askPlaceholder", "Ask about your farm (e.g. Should I irrigate Field A today?)...")}
              className="flex-1 p-3 rounded-2xl border border-slate-200 focus:outline-none focus:border-emerald-500 text-xs sm:text-sm bg-white"
            />

            <button
              onClick={() => handleSend()}
              className="p-3 rounded-2xl bg-slate-900 hover:bg-slate-800 text-white shadow-md transition-all"
            >
              <Send className="w-5 h-5" />
            </button>
          </div>
        </div>

      </div>

    </div>
  );
}
