import { useEffect, useRef, useState } from 'react';
import type { CoordinateType, EditRequest, FrozenCoordinate, ScanCoordinate } from './workbenchTypes';

export interface CoordinateDialogSelection {
  atoms: number[];
  frozen?: FrozenCoordinate;
  scan?: ScanCoordinate;
}

export function WorkbenchCoordinateDialog({ selection, kind, current, busy, error, onClose, onPreview, onDefine }: {
  selection: CoordinateDialogSelection;
  kind: CoordinateType;
  current: number;
  busy: boolean;
  error: string;
  onClose: () => void;
  onPreview: (edit: Omit<EditRequest, 'molecule'>) => void;
  onDefine: (coordinate: FrozenCoordinate | ScanCoordinate) => void;
}) {
  const dialog = useRef<HTMLDialogElement>(null);
  const targetInput = useRef<HTMLInputElement>(null);
  const [target, setTarget] = useState(selection.frozen ? String(selection.frozen.value) : current.toFixed(5));
  const [fixedSide, setFixedSide] = useState<'first' | 'last'>('first');
  const [moving, setMoving] = useState('');
  const [scanStart, setScanStart] = useState(selection.scan ? String(selection.scan.scan_start) : current.toFixed(5));
  const [scanEnd, setScanEnd] = useState(selection.scan ? String(selection.scan.scan_end) : '');
  const [scanSteps, setScanSteps] = useState(selection.scan ? String(selection.scan.scan_steps) : '');
  const [validationError, setValidationError] = useState('');
  const label = { bond: '距离', angle: '键角', dihedral: '二面角' }[kind];
  const unit = kind === 'bond' ? 'Å' : '°';

  useEffect(() => {
    const node = dialog.current!;
    const trigger = document.activeElement;
    node.showModal();
    targetInput.current?.focus();
    return () => {
      node.close();
      if (trigger instanceof HTMLElement && trigger.isConnected) trigger.focus();
    };
  }, []);

  const attempt = (operation: () => void) => {
    setValidationError('');
    try { operation(); } catch (reason) { setValidationError(reason instanceof Error ? reason.message : String(reason)); }
  };
  const number = (value: string, name: string) => {
    if (!value.trim() || !Number.isFinite(Number(value))) throw new Error(`请填写有限的${name}。`);
    return Number(value);
  };
  const preview = () => attempt(() => {
    const movingAtoms = moving.split(',').flatMap(part => part.trim().split(' ')).filter(Boolean).map(Number);
    if (moving.trim() && (!movingAtoms.length || movingAtoms.some(index => !Number.isInteger(index) || index < 1)
      || new Set(movingAtoms).size !== movingAtoms.length)) throw new Error('移动原子须为不重复的正整数编号，以逗号分隔。');
    onPreview({ action: 'coordinate', atoms: selection.atoms, value: number(target, '目标值'), fixed_side: fixedSide,
      ...(movingAtoms.length ? { moving_atoms: movingAtoms } : {}) });
  });

  return <dialog ref={dialog} className="wb-coordinate-dialog" aria-label={`调整${label}`}
    onCancel={event => { event.preventDefault(); if (!busy) onClose(); }}
    onClick={event => { if (event.target === event.currentTarget && !busy) {
      const bounds = event.currentTarget.getBoundingClientRect();
      if (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom) onClose();
    } }}>
    <form onSubmit={event => { event.preventDefault(); if (!busy) preview(); }}>
      <header className="wb-dialog-header"><h3>调整{label}</h3><button type="button" className="btn ghost sm" disabled={busy} aria-label="关闭内坐标编辑" onClick={onClose}>✕</button></header>
      <p className="wb-muted">原子顺序：{selection.atoms.join(' → ')}</p>
      <p className="wb-dialog-measure">当前{label} <strong>{current.toFixed(5)} {unit}</strong></p>
      {(validationError || error) && <p className="wb-error" role="alert">{validationError || error}</p>}
      <fieldset disabled={busy}>
        <label>目标值 {unit}<input ref={targetInput} aria-label="内坐标目标值" type="number" step="any" value={target} onChange={event => setTarget(event.target.value)} /></label>
        <label>固定侧<select value={fixedSide} onChange={event => setFixedSide(event.target.value as typeof fixedSide)}><option value="first">固定前侧，移动末侧基团</option><option value="last">固定末侧，移动前侧基团</option></select></label>
        <details><summary>手动指定移动部分</summary><label>手动指定移动原子（逗号分隔，可留空）<input value={moving} onChange={event => setMoving(event.target.value)} placeholder="如 4,5,6" /></label></details>
        <details open={!!selection.frozen || !!selection.scan}>
          <summary>冻结与扫描</summary>
          <button className="btn outline sm" type="button" onClick={() => attempt(() => onDefine({ coord_type: kind, atoms: selection.atoms, value: number(target, '目标值') }))}>定义冻结坐标</button>
          <div className="wb-row"><label>扫描起点<input type="number" step="any" value={scanStart} onChange={event => setScanStart(event.target.value)} /></label><label>终点<input type="number" step="any" value={scanEnd} onChange={event => setScanEnd(event.target.value)} /></label><label>步数<input type="number" min={1} value={scanSteps} onChange={event => setScanSteps(event.target.value)} /></label></div>
          <button className="btn outline sm" type="button" onClick={() => attempt(() => {
            const steps = number(scanSteps, '步数');
            if (!Number.isInteger(steps) || steps < 1) throw new Error('扫描步数须为正整数。');
            onDefine({ coord_type: kind, atoms: selection.atoms, scan_start: number(scanStart, '扫描起点'), scan_end: number(scanEnd, '扫描终点'), scan_steps: steps });
          })}>添加独立扫描坐标</button>
        </details>
      </fieldset>
      <footer className="wb-dialog-actions"><button type="button" className="btn outline sm" disabled={busy} onClick={onClose}>取消</button><button type="submit" className="btn green sm" disabled={busy}>{busy ? '正在调整…' : '预览结构调整'}</button></footer>
    </form>
  </dialog>;
}
