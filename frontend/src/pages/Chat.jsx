/**
 * Chat Page - Ci Chat Interface
 * Basic tap action target for CiButton
 */
import React from 'react';

export default function Chat() {
  return (
    <div className="p-8 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold text-gray-900 mb-4">
        💬 Чат з Ci
      </h1>
      <p className="mt-4 text-lg text-gray-700">
        Вітаємо в чат-інтерфейсі Ci — центральному комунікаційному модулі Cimeika.
      </p>
      
      <div className="mt-8 bg-indigo-50 border border-indigo-200 rounded-lg p-6">
        <h2 className="text-xl font-semibold text-indigo-900 mb-3">
          Функціонал чату
        </h2>
        <ul className="space-y-2 text-gray-700">
          <li>✨ Швидкий доступ до всіх модулів</li>
          <li>🔍 Пошук по всій системі</li>
          <li>💡 Підказки та рекомендації</li>
          <li>⚙️ Налаштування та управління</li>
          <li>📊 Огляд статистики та стану системи</li>
        </ul>
      </div>

      <div className="mt-8 bg-white border border-gray-200 rounded-lg p-6 shadow-sm">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">
          Як користуватися Ci-кнопкою?
        </h2>
        <div className="space-y-4 text-gray-700">
          <div className="flex items-start gap-3">
            <span className="text-2xl">👆</span>
            <div>
              <strong>Тап:</strong> Відкриває цей чат-інтерфейс
            </div>
          </div>
          <div className="flex items-start gap-3">
            <span className="text-2xl">↑</span>
            <div>
              <strong>Свайп вгору:</strong> ПоДія — події та активації
            </div>
          </div>
          <div className="flex items-start gap-3">
            <span className="text-2xl">↓</span>
            <div>
              <strong>Свайп вниз:</strong> Настрій — емоційні стани
            </div>
          </div>
          <div className="flex items-start gap-3">
            <span className="text-2xl">←</span>
            <div>
              <strong>Свайп вліво:</strong> Казкар — пам'ять та історії
            </div>
          </div>
          <div className="flex items-start gap-3">
            <span className="text-2xl">→</span>
            <div>
              <strong>Свайп вправо:</strong> Маля — ідеї та творчість
            </div>
          </div>
        </div>
      </div>

      <div className="mt-6 text-sm text-gray-500 text-center">
        <p>Ci-кнопка завжди доступна в правому нижньому куті екрану</p>
      </div>
    </div>
  );
}
