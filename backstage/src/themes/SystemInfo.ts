interface SystemInfo {
  system: string
  machine: string
  cpu: string
  cpu_percent: number
  memory_total: number
  memory_available: number
  disk_total: number
  disk_used: number
}

export type { SystemInfo }
