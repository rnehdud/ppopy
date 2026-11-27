import {createContext} from "react";

/** A local settings view lifetime, never authentication or consent authority.
 * Retirement blocks child callbacks synchronously before React unmounts them.
 * The parent owns this value; children must not revive or mutate it. */
export const AppSettingsLifetimeContext=createContext<{live:boolean}|null>(null);
