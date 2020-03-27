-- -*- lua -*-

help([[
Miniconda installation under home directory.
]])

local home = os.getenv("HOME")
local version = "latest"
local conda_home = pathJoin(home, "modules", "miniconda3")
local shell = myShellType()

if (mode() == "load") then
    execute {
        cmd = "source " .. conda_home .. "/etc/profile.d/conda." .. shell,
        modeA = { "load" }
    }
end

if (mode() == "unload") then
    execute {
        cmd = "unset CONDA_EXE; " ..
                "unset CONDA_DEFAULT_ENV; " ..
                "unset CONDA_PROMPT_MODIFIER; " ..
                "unset CONDA_PREFIX; " ..
                "unset CONDA_PYTHON_EXE; " ..
                "unset CONDA_SHLVL; " ..
                "unset _CONDA_ROOT; " ..
                "unset _CONDA_EXE; ",
        modeA = { "unload" }
    }

    if (shell == "csh") then
        execute {
            cmd = "unalias conda",
            modeA = { "unload" }
        }
    elseif (shell == "sh") then
        remove_path("PATH", pathJoin(conda_home, "condabin"))
        remove_path("PATH", pathJoin(conda_home, "bin"))
        remove_path("MANPATH", pathJoin(conda_home,"share","man"))
        execute {
            cmd = "unset _CE_CONDA; " ..
                    "unset _CE_M; ",
            modeA = { "unload" }
        }
        execute {
            cmd = "unset -f __conda_activate; " ..
                    "unset -f __conda_reactivate; " ..
                    "unset -f __conda_hashr; " ..
                    "unset -f conda; ",
            modeA = { "unload" }
        }
    end
end

whatis("Name         : Miniconda user install")
whatis("Version      : " .. version)
whatis("Category     : Compiler")
whatis("Description  : Python environment")
whatis("URL          : https://conda.io/miniconda")

family("python")
