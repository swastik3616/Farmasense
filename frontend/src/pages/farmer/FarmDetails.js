import React, { useEffect, useState, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getFarm, generateAdvisory, chatAdvisory } from '../../services/api';

const INDIAN_LANGUAGES = [
  "English", "Hindi", "Bengali", "Telugu", "Marathi", "Tamil", "Urdu", 
  "Gujarati", "Kannada", "Odia", "Punjabi", "Malayalam", "Assamese"
];

function FarmDetails() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [farm, setFarm] = useState(null);
  const [loading, setLoading] = useState(true);
  
  // Advisory & AI State
  const [language, setLanguage] = useState("English");
  const [advisory, setAdvisory] = useState(null);
  const [generating, setGenerating] = useState(false);
  
  // Chat State
  const [messages, setMessages] = useState([]);
  const [inputMsg, setInputMsg] = useState('');
  const [chatLoading, setChatLoading] = useState(false);
  const chatEndRef = useRef(null);

  useEffect(() => {
    fetchFarm();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id]);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const fetchFarm = async () => {
    try {
      const res = await getFarm(id);
      setFarm(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateAdvisory = async () => {
    setGenerating(true);
    try {
      const res = await generateAdvisory(id, language);
      setAdvisory(res.data);
    } catch (err) {
      alert(err.response?.data?.error || "Error generating advisory");
    } finally {
      setGenerating(false);
    }
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!inputMsg.trim()) return;

    const userMessage = { role: 'user', content: inputMsg };
    const historyPayload = messages.map(m => ({ role: m.role, content: m.content }));
    
    setMessages(prev => [...prev, userMessage]);
    setInputMsg('');
    setChatLoading(true);

    try {
      const res = await chatAdvisory(id, userMessage.content, language, historyPayload);
      setMessages(prev => [...prev, { role: 'ai', content: res.data.reply }]);
    } catch (err) {
      setMessages(prev => [...prev, { role: 'ai', content: "Error: " + (err.response?.data?.error || err.message) }]);
    } finally {
      setChatLoading(false);
    }
  };

  if (loading) return <div style={{ padding: 40, textAlign: 'center' }}>Loading Farm Details...</div>;
  if (!farm) return <div style={{ padding: 40, textAlign: 'center' }}>Farm not found.</div>;

  return (
    <div style={{ paddingBottom: '80px' }}>
      <div className="page-header" style={{ marginBottom: '16px' }}>
        <h1 className="page-title">{farm.name || "My Farm"}</h1>
        <button className="btn" style={{ width: 'auto', background: 'var(--gray-light)', padding: '10px 16px' }} onClick={() => navigate('/farmer/farms')}>
          Back
        </button>
      </div>

      <div className="stat-card" style={{ marginBottom: '20px' }}>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '16px', justifyContent: 'space-between' }}>
          <div>
            <div className="stat-label">Location</div>
            <div style={{ fontWeight: 600 }}>{farm.district}, {farm.state}</div>
          </div>
          <div>
            <div className="stat-label">Size</div>
            <div style={{ fontWeight: 600 }}>{farm.land_size_acres} Acres</div>
          </div>
          <div>
            <div className="stat-label">Soil & Water</div>
            <div style={{ fontWeight: 600 }}>{farm.soil_type} • {farm.water_source}</div>
          </div>
          <div>
            <div className="stat-label">AI Language</div>
            <select 
              className="form-control" 
              style={{ width: 'auto', padding: '6px 12px', minWidth: '120px' }}
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
            >
              {INDIAN_LANGUAGES.map(lang => (
                <option key={lang} value={lang}>{lang}</option>
              ))}
            </select>
          </div>
        </div>
      </div>

      <div className="auth-card" style={{ maxWidth: '100%', marginBottom: '20px', padding: '24px', textAlign: 'left' }}>
        <h3 style={{ marginTop: 0 }}>Smart Advisory Report</h3>
        {!advisory ? (
          <div>
            <p style={{ color: 'var(--gray)' }}>Get an AI-powered crop recommendation report explicitly tailored to your farm's soil, region, and size. Written in {language}.</p>
            <button className="btn btn-primary" onClick={handleGenerateAdvisory} disabled={generating} style={{ width: 'auto' }}>
              {generating ? 'Analyzing data...' : `Generate Advisory (${language})`}
            </button>
          </div>
        ) : (
          <div>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px', marginBottom: '16px', background: 'var(--gray-light)', padding: '16px', borderRadius: '12px' }}>
              <div><strong>Season:</strong> {advisory.season}</div>
              <div><strong>Top Crop:</strong> {advisory.full_advisory?.recommended_crop}</div>
              <div><strong>Secondary:</strong> {advisory.full_advisory?.second_option_crop}</div>
              <div><strong>Avoid:</strong> {advisory.full_advisory?.avoid_crop}</div>
            </div>
            
            <p style={{ lineHeight: 1.6 }}>
              {advisory.full_advisory?.final_advisory}
            </p>
            <button className="btn" style={{ width: 'auto', background: 'var(--gray-light)', marginTop: '10px' }} onClick={handleGenerateAdvisory} disabled={generating}>
              {generating ? 'Regenerating...' : 'Regenerate Advisory'}
            </button>
          </div>
        )}
      </div>

      <div className="auth-card" style={{ maxWidth: '100%', padding: 0, overflow: 'hidden', display: 'flex', flexDirection: 'column' }}>
        <div style={{ padding: '16px', background: 'var(--primary-dark)', color: 'white' }}>
          <h3 style={{ margin: 0, color: 'white' }}>Farm Assistant</h3>
          <p style={{ margin: 0, fontSize: '0.85rem', opacity: 0.9 }}>Ask me anything about your farm in {language}</p>
        </div>
        
        <div style={{ height: '350px', overflowY: 'auto', padding: '16px', background: '#f5f7f5', display: 'flex', flexDirection: 'column', gap: '12px' }}>
          {messages.length === 0 && (
            <div style={{ textAlign: 'center', color: 'var(--gray)', marginTop: '40px' }}>
              Say hello! The AI knows your farm's soil, location, and size.
            </div>
          )}
          
          {messages.map((msg, idx) => (
            <div key={idx} style={{
              alignSelf: msg.role === 'user' ? 'flex-end' : 'flex-start',
              background: msg.role === 'user' ? 'var(--primary)' : 'white',
              color: msg.role === 'user' ? 'white' : 'var(--dark)',
              padding: '10px 14px',
              borderRadius: '16px',
              borderBottomRightRadius: msg.role === 'user' ? '4px' : '16px',
              borderBottomLeftRadius: msg.role === 'ai' ? '4px' : '16px',
              maxWidth: '85%',
              boxShadow: '0 2px 4px rgba(0,0,0,0.05)',
              lineHeight: 1.5
            }}>
              {msg.content}
            </div>
          ))}
          {chatLoading && (
            <div style={{ alignSelf: 'flex-start', background: 'white', padding: '10px 14px', borderRadius: '16px', boxShadow: '0 2px 4px rgba(0,0,0,0.05)' }}>
              typing...
            </div>
          )}
          <div ref={chatEndRef} />
        </div>

        <form onSubmit={handleSendMessage} style={{ display: 'flex', padding: '12px', background: 'white', borderTop: '1px solid var(--gray-light)' }}>
          <input 
            type="text" 
            placeholder={`Type in ${language}...`}
            value={inputMsg}
            onChange={(e) => setInputMsg(e.target.value)}
            style={{ flexGrow: 1, padding: '12px', borderRadius: '24px', border: '1px solid var(--gray-light)', outline: 'none' }}
          />
          <button 
            type="submit" 
            className="btn btn-primary" 
            style={{ width: '48px', height: '48px', borderRadius: '50%', padding: 0, marginLeft: '8px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}
            disabled={chatLoading}
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <line x1="22" y1="2" x2="11" y2="13"></line>
              <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
            </svg>
          </button>
        </form>
      </div>
    </div>
  );
}

export default FarmDetails;
