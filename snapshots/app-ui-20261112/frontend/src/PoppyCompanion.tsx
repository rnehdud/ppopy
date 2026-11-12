import "./poppyCompanion.css";

export type PoppyCompanionState = "idle" | "greeting" | "thinking";

type Props = {
  state?: PoppyCompanionState;
  size?: number;
  /** Leave empty when nearby text already describes the character. */
  label?: string;
  paused?: boolean;
  className?: string;
};

/** Decorative companion. Its animation does not indicate analysis progress. */
export function PoppyCompanion({
  state = "idle", size = 96, label = "", paused = false, className = "",
}: Props) {
  return (
    <span
      className={`poppy-companion ${className}`.trim()}
      data-state={state}
      data-paused={paused || undefined}
      style={{ width: size }}
    >
      <img
        src={`${import.meta.env.BASE_URL}characters/popo-v1.png`}
        width={1254}
        height={1254}
        alt={label}
        draggable={false}
        decoding="async"
      />
    </span>
  );
}
