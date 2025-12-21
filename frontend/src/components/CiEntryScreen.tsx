/**
 * Ci Entry Screen - CANON v1.0.0 Implementation
 * Single entry point for Cimeika
 * Goal: user_action_in_<=5s
 * 
 * Forbidden: menus, onboarding, explanations, login_required, feature_lists
 */
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './CiEntryScreen.css';

interface CaptureResult {
  event_id: string;
  event: any;
  time_position: string;
  related_traces: any[];
}

const CiEntryScreen: React.FC = () => {
  const navigate = useNavigate();
  const [captureText, setCaptureText] = useState('');
  const [isCapturing, setIsCapturing] = useState(false);
  const [captureResult, setCaptureResult] = useState<CaptureResult | null>(null);

  const handleCapture = async () => {
    if (!captureText.trim()) return;
    
    setIsCapturing(true);
    
    try {
      const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:5000';
      const response = await fetch(`${API_BASE}/api/v1/ci/capture`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          type: 'text',
          content: captureText
        })
      });
      
      const result = await response.json();
      setCaptureResult(result);
      setCaptureText('');
    } catch (error) {
      console.error('Capture failed:', error);
    } finally {
      setIsCapturing(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !isCapturing) {
      handleCapture();
    }
  };

  const handleExpand = (option: string) => {
    switch (option) {
      case 'calendar':
        navigate('/calendar');
        break;
      case 'gallery':
        navigate('/gallery');
        break;
      case 'narrative':
        navigate('/kazkar');
        break;
      case 'close':
        setCaptureResult(null);
        break;
    }
  };

  if (captureResult) {
    // Step 2: Reveal
    return (
      <div className="ci-entry-screen ci-reveal">
        <div className="ci-reveal-content">
          <div className="ci-reveal-event">
            <p>{captureResult.event?.content}</p>
          </div>
          
          <div className="ci-reveal-time">
            {captureResult.time_position}
          </div>

          {captureResult.related_traces?.length > 0 && (
            <div className="ci-reveal-traces">
              {captureResult.related_traces.map((trace: any, idx: number) => (
                <div key={idx} className="ci-trace-item">
                  {trace.title}
                </div>
              ))}
            </div>
          )}

          {/* Step 3: Expand options */}
          <div className="ci-expand-options">
            <button onClick={() => handleExpand('calendar')} className="ci-option-btn">
              Calendar
            </button>
            <button onClick={() => handleExpand('gallery')} className="ci-option-btn">
              Gallery
            </button>
            <button onClick={() => handleExpand('narrative')} className="ci-option-btn">
              Kazkar
            </button>
            <button onClick={() => handleExpand('close')} className="ci-option-btn ci-close">
              ×
            </button>
          </div>
        </div>
      </div>
    );
  }

  // Step 0: Contact - Entry screen
  return (
    <div className="ci-entry-screen">
      <div className="ci-logo-container">
        <div className="ci-logo">Ci</div>
      </div>
      
      <div className="ci-action-container">
        <input
          type="text"
          className="ci-input"
          placeholder=""
          value={captureText}
          onChange={(e) => setCaptureText(e.target.value)}
          onKeyPress={handleKeyPress}
          disabled={isCapturing}
          autoFocus
        />
      </div>

      <div className="ci-hint">Mark the moment</div>
    </div>
  );
};

export default CiEntryScreen;
