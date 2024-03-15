/*
 * SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
 *
 * SPDX-FileContributor: Philip Abbet <philip.abbet@idiap.ch>
 *
 * SPDX-License-Identifier: GPL-3.0-only
 */

#include "utils.h"
#include <dlfcn.h>


std::filesystem::path getRuntimePath()
{
    Dl_info info;
    if (dladdr((const void*) &getRuntimePath, &info)) {
        std::filesystem::path path(info.dli_fname);
        std::filesystem::path folder = path.remove_filename();
        return folder;
    }

    return std::filesystem::current_path();
}


std::string getAssetsPath()
{
    std::filesystem::path path = getRuntimePath();
    return (path / "assets" / "").string();
}
