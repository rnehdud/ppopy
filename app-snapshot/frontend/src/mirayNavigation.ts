import config from "../../skin_engine/config/miray_navigation.json";

export type MirayTab = "cosmetics" | "routine" | "home" | "explore" | "my";
export type HomeTask = {id: string; kind: string; title: string; route: MirayTab};
export function visibleHomeTasks(tasks: HomeTask[]): HomeTask[] {
  const unique = tasks.filter((task, index) => tasks.findIndex(item => item.id === task.id) === index);
  const priority = (kind: string) => {
    const index = config.task_priority.indexOf(kind);
    return index < 0 ? config.task_priority.length : index;
  };
  return unique.sort((a, b) => priority(a.kind) - priority(b.kind)).slice(0, config.home_task_limit);
}
