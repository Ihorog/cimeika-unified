'use client';

import { useEffect, useRef, useState } from 'react';
import styles from './RootEntrance.module.css';

type Phase = 'rest' | 'approach' | 'contact' | 'resonance' | 'open';

const CI_MARK = 'https://raw.githubusercontent.com/Ihorog/media/main/Ci.png';

export function RootEntrance() {
  const surfaceRef = useRef<HTMLElement>(null);
  const timersRef = useRef<number[]>([]);
  const [phase, setPhase] = useState<Phase>('rest');

  useEffect(() => {
    const previousOverflow = document.body.style.overflow;
    document.body.style.overflow = 'hidden';

    return () => {
      document.body.style.overflow = previousOverflow;
      timersRef.current.forEach(window.clearTimeout);
    };
  }, []);

  const clearTimers = () => {
    timersRef.current.forEach(window.clearTimeout);
    timersRef.current = [];
  };

  const setPointer = (clientX: number, clientY: number) => {
    const surface = surfaceRef.current;
    if (!surface) return;

    const rect = surface.getBoundingClientRect();
    const x = Math.max(0, Math.min(1, (clientX - rect.left) / rect.width));
    const y = Math.max(0, Math.min(1, (clientY - rect.top) / rect.height));

    surface.style.setProperty('--pointer-x', `${x * 100}%`);
    surface.style.setProperty('--pointer-y', `${y * 100}%`);
    surface.style.setProperty('--drift-x', `${(x - 0.5) * 10}px`);
    surface.style.setProperty('--drift-y', `${(y - 0.5) * 8}px`);
  };

  const activate = () => {
    clearTimers();
    setPhase('contact');

    timersRef.current.push(
      window.setTimeout(() => setPhase('resonance'), 120),
      window.setTimeout(() => setPhase('open'), 1120),
    );
  };

  return (
    <section
      ref={surfaceRef}
      className={styles.surface}
      data-phase={phase}
      aria-label="Cimeika"
      onPointerMove={(event) => setPointer(event.clientX, event.clientY)}
    >
      <div className={styles.ambient} aria-hidden="true" />
      <div className={styles.opticalField} aria-hidden="true">
        <span className={styles.coldField} />
        <span className={styles.warmField} />
        <span className={styles.axis} />
        <span className={`${styles.arc} ${styles.arcOne}`} />
        <span className={`${styles.arc} ${styles.arcTwo}`} />
        <span className={`${styles.arc} ${styles.arcThree}`} />
        <span className={styles.memoryTrace} />
      </div>

      <div className={styles.identity}>
        <button
          type="button"
          className={styles.markButton}
          aria-label="Відкрити Cimeika"
          aria-pressed={phase === 'open'}
          onPointerEnter={() => {
            if (phase === 'rest') setPhase('approach');
          }}
          onPointerLeave={() => {
            if (phase === 'approach') setPhase('rest');
          }}
          onPointerDown={() => {
            if (phase !== 'resonance') setPhase('contact');
          }}
          onClick={activate}
        >
          <span className={styles.markHalo} aria-hidden="true" />
          <img
            className={styles.mark}
            src={CI_MARK}
            alt=""
            width="512"
            height="512"
            draggable="false"
          />
        </button>

        <h1 className={styles.wordmark}>Cimeika</h1>
      </div>

      <div className={styles.edgeSignature} aria-hidden="true">
        <span />
      </div>
    </section>
  );
}
