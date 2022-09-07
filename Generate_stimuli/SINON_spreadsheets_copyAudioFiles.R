# save only if not previously saved
if (!dir.exists(paste0(dirout,'/files'))){
  dir.create(paste0(dirout,'/files'))
  file.copy(paste0(audiofiles_sissn,filessissn[which(filessissn %in% ds$file)]),paste0(dirout,'/files'))
  file.copy(paste0(audiofiles_nvoc,filesnvoc[which(filesnvoc %in% ds$file)]),paste0(dirout,'/files'))
}

`%nin%` = Negate(`%in%`)