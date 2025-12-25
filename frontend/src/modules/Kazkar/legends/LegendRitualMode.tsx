/**
 * LegendRitualMode.tsx
 * Meditative mode with breathing animations and symbolic text
 */
import React from 'react';
import { motion } from 'framer-motion';

interface LegendRitualModeProps {
  onReturn: () => void;
}

const LegendRitualMode: React.FC<LegendRitualModeProps> = ({ onReturn }) => {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 1.5 }}
      style={{
        minHeight: '100vh',
        background: 'linear-gradient(to bottom, #1e1b4b, #312e81, #4c1d95)',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '2rem',
        position: 'relative',
      }}
    >
      {/* Breathing glow effect */}
      <motion.div
        animate={{
          opacity: [0.3, 0.6, 0.3],
          scale: [1, 1.2, 1],
        }}
        transition={{
          duration: 4,
          repeat: Infinity,
          ease: 'easeInOut',
        }}
        style={{
          position: 'absolute',
          width: '400px',
          height: '400px',
          borderRadius: '50%',
          background: 'radial-gradient(circle, rgba(99, 102, 241, 0.4), transparent)',
          filter: 'blur(60px)',
          pointerEvents: 'none',
        }}
      />

      {/* Content */}
      <motion.div
        initial={{ y: 20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ delay: 0.5, duration: 1 }}
        style={{
          maxWidth: '700px',
          textAlign: 'center',
          zIndex: 1,
        }}
      >
        {/* Symbolic lines with breathing effect */}
        <motion.div
          animate={{
            opacity: [0.7, 1, 0.7],
          }}
          transition={{
            duration: 4,
            repeat: Infinity,
            ease: 'easeInOut',
          }}
          style={{
            fontSize: '2rem',
            lineHeight: '2',
            color: '#e0e7ff',
            marginBottom: '3rem',
            fontWeight: '300',
            letterSpacing: '0.05em',
          }}
        >
          <div style={{ marginBottom: '2rem' }}>Зупинись. Послухай.</div>
          <div>Якщо відчуєш іскру — дай їй напрям.</div>
        </motion.div>

        {/* Decorative symbol */}
        <motion.div
          animate={{
            rotate: [0, 360],
            opacity: [0.5, 0.8, 0.5],
          }}
          transition={{
            rotate: { duration: 20, repeat: Infinity, ease: 'linear' },
            opacity: { duration: 4, repeat: Infinity, ease: 'easeInOut' },
          }}
          style={{
            fontSize: '4rem',
            marginBottom: '3rem',
            color: '#818cf8',
          }}
        >
          ✦
        </motion.div>

        {/* Return button */}
        <motion.button
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 2, duration: 0.8 }}
          onClick={onReturn}
          style={{
            background: 'rgba(99, 102, 241, 0.2)',
            border: '1px solid rgba(139, 92, 246, 0.5)',
            borderRadius: '12px',
            padding: '1rem 2rem',
            fontSize: '1rem',
            fontWeight: '600',
            color: '#c7d2fe',
            cursor: 'pointer',
            boxShadow: '0 4px 12px rgba(79, 70, 229, 0.3)',
            transition: 'transform 0.2s, background 0.2s',
            display: 'inline-flex',
            alignItems: 'center',
            gap: '0.5rem',
          }}
          whileHover={{
            scale: 1.05,
            background: 'rgba(99, 102, 241, 0.3)',
          }}
          whileTap={{ scale: 0.95 }}
        >
          <span>🔙</span>
          <span>Повернутись до легенди</span>
        </motion.button>
      </motion.div>
    </motion.div>
  );
};

export default LegendRitualMode;
