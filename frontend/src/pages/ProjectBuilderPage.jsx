import React, { useState, useEffect } from 'react';
import { 
  Sparkles, 
  Folder, 
  FileCode, 
  Play, 
  Save, 
  RefreshCw, 
  Eye, 
  Code, 
  Check, 
  Plus,
  Terminal,
  ExternalLink
} from 'lucide-react';
import { api } from '../services/api';

export default function ProjectBuilderPage() {
  const [projects, setProjects] = useState([]);
  const [selectedProject, setSelectedProject] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);
  const [fileContent, setFileContent] = useState('');
  const [prompt, setPrompt] = useState('Create an interactive Pathfinding Visualizer with BFS and obstacles in HTML/JS');
  const [generating, setGenerating] = useState(false);
  const [saving, setSaving] = useState(false);
  const [savedSuccess, setSavedSuccess] = useState(false);
  const [viewMode, setViewMode] = useState('preview'); // 'preview' or 'split'

  useEffect(() => {
    loadProjects();
  }, []);

  async function loadProjects() {
    try {
      const data = await api.listProjects();
      setProjects(data);
      if (data.length > 0) {
        selectProject(data[0].id);
      }
    } catch (err) {
      console.error('Failed to load projects:', err);
    }
  }

  async function selectProject(id) {
    try {
      const proj = await api.getProject(id);
      setSelectedProject(proj);
      if (proj.files && proj.files.length > 0) {
        setSelectedFile(proj.files[0]);
        setFileContent(proj.files[0].content);
      }
    } catch (err) {
      console.error('Failed to get project:', err);
    }
  }

  async function handleGenerate() {
    if (!prompt.trim() || generating) return;
    setGenerating(true);
    try {
      const newProj = await api.generateProject(prompt);
      setProjects(prev => [newProj, ...prev]);
      setSelectedProject(newProj);
      if (newProj.files && newProj.files.length > 0) {
        setSelectedFile(newProj.files[0]);
        setFileContent(newProj.files[0].content);
      }
    } catch (err) {
      console.error('Project generation error:', err);
    } finally {
      setGenerating(false);
    }
  }

  async function handleSaveFile() {
    if (!selectedProject || !selectedFile || saving) return;
    setSaving(true);
    try {
      await api.updateProjectFile(selectedProject.id, selectedFile.filename, {
        filename: selectedFile.filename,
        filepath: selectedFile.filepath,
        content: fileContent,
        language: selectedFile.language
      });
      setSavedSuccess(true);
      setTimeout(() => setSavedSuccess(false), 2000);
      
      // Update local file object in project state
      setSelectedProject(prev => ({
        ...prev,
        files: prev.files.map(f => f.filename === selectedFile.filename ? { ...f, content: fileContent } : f)
      }));
    } catch (err) {
      console.error('Save error:', err);
    } finally {
      setSaving(false);
    }
  }

  function handleSelectFile(file) {
    setSelectedFile(file);
    setFileContent(file.content);
  }

  // Construct srcDoc for live iframe preview
  function getPreviewSrcDoc() {
    if (!selectedProject || !selectedProject.files) return '';
    const htmlFile = selectedProject.files.find(f => f.filename.endsWith('.html'));
    const cssFile = selectedProject.files.find(f => f.filename.endsWith('.css'));
    const jsFile = selectedProject.files.find(f => f.filename.endsWith('.js'));

    if (!htmlFile) {
      return `<html><body style="background:#0b0f19;color:#fff;font-family:sans-serif;padding:2rem;">
        <h3>Python / CLI Script Project</h3>
        <p>This is a backend algorithm script. You can edit and test files in the editor.</p>
      </body></html>`;
    }

    let html = htmlFile.content;
    if (cssFile) {
      html = html.replace('</head>', `<style>${cssFile.content}</style></head>`);
    }
    if (jsFile) {
      html = html.replace('</body>', `<script>${jsFile.content}</script></body>`);
    }
    return html;
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem', height: 'calc(100vh - 100px)' }}>
      {/* Top Natural Language Generator Prompt Bar */}
      <div className="card-glass" style={{ padding: '1rem 1.5rem', display: 'flex', alignItems: 'center', gap: '1rem', flexWrap: 'wrap' }}>
        <div style={{
          width: '36px',
          height: '36px',
          borderRadius: '8px',
          background: 'linear-gradient(135deg, #0284c7 0%, #38bdf8 100%)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          color: '#fff',
          flexShrink: 0
        }}>
          <Sparkles size={18} />
        </div>

        <input
          type="text"
          placeholder="Describe your algorithm project idea (e.g. 'Build an interactive Binary Search Tree with insertion & animations')..."
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          style={{
            flex: 1,
            minWidth: '280px',
            padding: '0.65rem 1rem',
            borderRadius: '10px',
            border: '1px solid var(--border-subtle)',
            backgroundColor: 'var(--bg-primary)',
            color: 'var(--text-primary)',
            fontSize: '0.88rem',
            outline: 'none'
          }}
        />

        <button
          onClick={handleGenerate}
          disabled={generating || !prompt.trim()}
          className="btn-primary"
          style={{ padding: '0.65rem 1.25rem', whiteSpace: 'nowrap' }}
        >
          {generating ? 'Synthesizing Project...' : 'Generate Project with AI'}
        </button>
      </div>

      {/* Main Workspace: File Tree (220px), Editor (flex), Live Preview (flex) */}
      <div style={{ display: 'grid', gridTemplateColumns: '240px 1fr 1fr', gap: '1rem', flex: 1, minHeight: 0 }}>
        {/* 1. Left Project & File Explorer */}
        <div className="card-glass" style={{ padding: '1rem', display: 'flex', flexDirection: 'column', gap: '1rem', overflowY: 'auto' }}>
          <div>
            <div style={{ fontSize: '0.72rem', fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: '0.4rem' }}>
              Saved Projects ({projects.length})
            </div>
            <select
              value={selectedProject?.id || ''}
              onChange={(e) => selectProject(Number(e.target.value))}
              style={{
                width: '100%',
                padding: '0.45rem',
                borderRadius: '6px',
                border: '1px solid var(--border-subtle)',
                backgroundColor: 'var(--bg-primary)',
                color: 'var(--text-primary)',
                fontSize: '0.82rem',
                outline: 'none',
                cursor: 'pointer'
              }}
            >
              {projects.map(p => (
                <option key={p.id} value={p.id}>{p.title}</option>
              ))}
            </select>
          </div>

          <div style={{ flex: 1 }}>
            <div style={{ fontSize: '0.72rem', fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: '0.5rem' }}>
              Project Files
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
              {(selectedProject?.files || []).map((file, idx) => {
                const isSelected = selectedFile?.filename === file.filename;
                return (
                  <button
                    key={idx}
                    onClick={() => handleSelectFile(file)}
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: '0.5rem',
                      padding: '0.5rem 0.65rem',
                      borderRadius: '6px',
                      border: isSelected ? '1px solid var(--accent-cyan)' : '1px solid transparent',
                      backgroundColor: isSelected ? 'rgba(56, 189, 248, 0.15)' : 'transparent',
                      color: isSelected ? 'var(--accent-cyan)' : 'var(--text-secondary)',
                      fontSize: '0.82rem',
                      fontFamily: 'Consolas, monospace',
                      textAlign: 'left',
                      cursor: 'pointer'
                    }}
                  >
                    <FileCode size={14} />
                    <span style={{ flex: 1, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                      {file.filename}
                    </span>
                  </button>
                );
              })}
            </div>
          </div>
        </div>

        {/* 2. Center Code Editor */}
        <div className="card-glass" style={{ display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
          <div style={{
            padding: '0.65rem 1rem',
            borderBottom: '1px solid var(--border-subtle)',
            backgroundColor: 'var(--bg-card)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between'
          }}>
            <span style={{ fontSize: '0.85rem', fontWeight: 700, fontFamily: 'Consolas, monospace', color: 'var(--accent-cyan)' }}>
              {selectedFile?.filename || 'No file selected'}
            </span>

            <button
              onClick={handleSaveFile}
              disabled={saving}
              className="btn-secondary"
              style={{ padding: '0.35rem 0.75rem', fontSize: '0.78rem' }}
            >
              {savedSuccess ? <Check size={14} color="#10b981" /> : <Save size={14} />}
              <span>{savedSuccess ? 'Saved!' : 'Save Code'}</span>
            </button>
          </div>

          <textarea
            value={fileContent}
            onChange={(e) => setFileContent(e.target.value)}
            spellCheck="false"
            style={{
              flex: 1,
              padding: '1rem',
              backgroundColor: '#070b14',
              color: '#f8fafc',
              fontFamily: 'Consolas, Monaco, monospace',
              fontSize: '0.86rem',
              lineHeight: 1.5,
              border: 'none',
              outline: 'none',
              resize: 'none'
            }}
          />
        </div>

        {/* 3. Right Live In-Browser Sandbox Preview */}
        <div className="card-glass" style={{ display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
          <div style={{
            padding: '0.65rem 1rem',
            borderBottom: '1px solid var(--border-subtle)',
            backgroundColor: 'var(--bg-card)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', fontSize: '0.85rem', fontWeight: 700, color: 'var(--text-primary)' }}>
              <Eye size={15} color="var(--accent-emerald)" />
              <span>Interactive Live Preview</span>
            </div>

            <span style={{ fontSize: '0.72rem', color: 'var(--accent-emerald)', display: 'flex', alignItems: 'center', gap: '4px' }}>
              <span style={{ width: '6px', height: '6px', borderRadius: '50%', backgroundColor: 'var(--accent-emerald)' }} />
              Sandbox Active
            </span>
          </div>

          <div style={{ flex: 1, backgroundColor: '#ffffff', position: 'relative' }}>
            <iframe
              title="Project Live Preview"
              srcDoc={getPreviewSrcDoc()}
              style={{
                width: '100%',
                height: '100%',
                border: 'none'
              }}
              sandbox="allow-scripts"
            />
          </div>
        </div>
      </div>
    </div>
  );
}
