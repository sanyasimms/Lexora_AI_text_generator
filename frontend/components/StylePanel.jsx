export default function StylePanel({ styles, targetLanguage, onStyleChange, onTargetLanguageChange, languageOptions }) {
  const updateStyle = (field, value) => {
    onStyleChange({ ...styles, [field]: value });
  };

  return (
    <section className="panel">
      <div className="panel__header">
        <div>
          <p className="panel__eyebrow">Style</p>
          <h2>Caption treatment</h2>
        </div>
      </div>

      <div className="field-grid">
        <label className="field">
          <span>Target language</span>
          <select value={targetLanguage} onChange={(event) => onTargetLanguageChange(event.target.value)}>
            {languageOptions.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </label>

        <label className="field">
          <span>Font family</span>
          <input value={styles.font_family} onChange={(event) => updateStyle('font_family', event.target.value)} />
        </label>

        <label className="field">
          <span>Font size: {styles.font_size}px</span>
          <input
            type="range"
            min="18"
            max="84"
            value={styles.font_size}
            onChange={(event) => updateStyle('font_size', Number(event.target.value))}
          />
        </label>

        <label className="field field--split">
          <span>Text color</span>
          <input type="color" value={styles.text_color} onChange={(event) => updateStyle('text_color', event.target.value)} />
        </label>

        <label className="field field--split">
          <span>Background</span>
          <input
            type="color"
            value={styles.background_color}
            onChange={(event) => updateStyle('background_color', event.target.value)}
          />
        </label>

        <label className="field field--full">
          <span>Background opacity: {styles.bg_opacity.toFixed(2)}</span>
          <input
            type="range"
            min="0"
            max="1"
            step="0.05"
            value={styles.bg_opacity}
            onChange={(event) => updateStyle('bg_opacity', Number(event.target.value))}
          />
        </label>
      </div>
    </section>
  );
}