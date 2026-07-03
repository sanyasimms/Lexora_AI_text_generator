import { useState } from 'react';

export default function UploadDropzone({
  onFileSelect,
  onTranscribe,
  onExport,
  isTranscribing,
  isExporting,
  status,
  error,
  fileName,
  hasVideo,
}) {
  const [isDragging, setIsDragging] = useState(false);

  const handleFile = (file) => {
    if (file) {
      onFileSelect(file);
    }
  };

  return (
    <section className="panel panel--upload">
      <div className="panel__header">
        <div>
          <p className="panel__eyebrow">Upload</p>
          <h2>Choose a source clip</h2>
        </div>
        <div className="upload-pill">MP4, MOV, MKV, WEBM</div>
      </div>

      <label
        className={`dropzone ${isDragging ? 'dropzone--active' : ''}`}
        onDragEnter={(event) => {
          event.preventDefault();
          setIsDragging(true);
        }}
        onDragOver={(event) => {
          event.preventDefault();
          setIsDragging(true);
        }}
        onDragLeave={(event) => {
          event.preventDefault();
          setIsDragging(false);
        }}
        onDrop={(event) => {
          event.preventDefault();
          setIsDragging(false);
          handleFile(event.dataTransfer.files?.[0]);
        }}
      >
        <input
          type="file"
          accept="video/mp4,video/quicktime,video/x-matroska,video/webm"
          onChange={(event) => {
            handleFile(event.target.files?.[0]);
          }}
        />
        <span className="dropzone__title">Drop a video here or browse</span>
        <span className="dropzone__copy">The selected file is passed straight to the transcription endpoint.</span>
        <span className="dropzone__file">{fileName || 'No file selected yet'}</span>
      </label>

      <div className="panel__actions">
        <button
          className="button button--secondary"
          type="button"
          onClick={onTranscribe}
          disabled={isTranscribing || !hasVideo}
        >
          {isTranscribing ? 'Transcribing...' : 'Generate subtitles'}
        </button>
        <button className="button" type="button" onClick={onExport} disabled={isExporting || !hasVideo}>
          {isExporting ? 'Rendering...' : 'Export final video'}
        </button>
      </div>

      <div className="status-card">
        <p className="status-card__label">Status</p>
        <p>{status}</p>
        {error ? <p className="status-card__error">{error}</p> : null}
      </div>
    </section>
  );
}