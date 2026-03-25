import type { ModuleInterface, ModuleStatus, ModuleMetadata } from '../../types';

const galleryModule: ModuleInterface = {
  getName: () => 'gallery',
  getStatus: async (): Promise<ModuleStatus> => ({
    status: 'active',
    name: 'gallery',
    initialized: true,
  }),
  initialize: async () => true,
  getMetadata: (): ModuleMetadata => ({
    name: 'gallery',
    version: '0.1.0',
    description: 'Cimeika Gallery media module',
  }),
};

export { galleryModule };
