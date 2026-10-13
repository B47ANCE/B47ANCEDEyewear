B47ANCEDEyewear = B47ANCEDEyewear or {}
B47ANCEDEyewear.TestKit = B47ANCEDEyewear.TestKit or {}

local TestKit = B47ANCEDEyewear.TestKit
local MARKER = "B47ANCEDEyewear.TestKitVersion"
local VERSION = "1"
local CONTENTS = {
    { "Base.Glasses", 1 }, { "Base.Glasses_Prescription", 1 },
    { "Base.Glasses_Aviators", 1 }, { "Base.Glasses_Prescription_Aviators", 1 },
    { "Base.Glasses_Normal", 1 }, { "Base.Glasses_Cosmetic_Normal", 1 },
    { "Base.Glasses_Reading", 1 }, { "Base.Glasses_SafetyGoggles", 1 },
    { "Base.Glasses_Shooting", 1 }, { "Base.Glasses_Prescription_Shooting", 1 },
    { "Base.Glasses_SkiGoggles", 1 }, { "Base.Glasses_Sun", 1 },
    { "Base.Glasses_Prescription_Sun", 1 }, { "Base.Glasses_SwimmingGoggles", 1 },
    { "Base.Glasses_CatsEye", 1 }, { "Base.Glasses_CatsEye_Sun", 1 },
    { "Base.Glasses_Cosmetic_CatsEye", 1 }, { "Base.Glasses_Prescription_CatsEye_Sun", 1 },
    { "Base.Glasses_Normal_HornRimmed", 1 }, { "Base.Glasses_Cosmetic_Normal_HornRimmed", 1 },
    { "Base.Glasses_JackieO", 1 }, { "Base.Glasses_Prescription_JackieO", 1 },
    { "Base.Glasses_Macho", 1 }, { "Base.Glasses_Round_Normal", 1 },
    { "Base.Glasses_Round_Shades", 1 }, { "Base.Glasses_Cosmetic_Round_Normal", 1 },
    { "Base.Glasses_Prescription_Round_Shades", 1 }, { "Base.Glasses_70s_Gold", 1 },
    { "Base.Glasses_Cosmetic_70s_Gold", 1 }, { "Base.Glasses_Round_HoloSkulls", 1 },
    { "Base.Glasses_OldWeldingGoggles", 1 }, { "Base.Glasses_HalfMoon", 1 },
    { "Base.Glasses_Cosmetic_HalfMoon", 1 }, { "Base.Glasses_MonocleLeft", 1 },
    { "Base.Glasses_MonocleRight", 1 }, { "Base.Glasses_Cosmetic_MonocleLeft", 1 },
    { "Base.Glasses_Cosmetic_MonocleRight", 1 }, { "Base.Glasses_SunCheap", 1 },
    { "Base.Glasses_3dGlasses", 1 }, { "Base.Glasses_Groucho", 1 },
    { "Base.Glasses_Venetian", 1 }, { "Base.Glasses_NewWave", 1 },
    { "Base.Glasses_Novelty_Xray", 1 },
    { "AuthenticZClothing.Glasses_AviatorsSunset", 1 }, { "AuthenticZClothing.Glasses_Cheese", 1 },
    { "AuthenticZClothing.Glasses_ReadingBlack", 1 }, { "AuthenticZClothing.Glasses_Popeyes", 1 },
    { "AuthenticZClothing.Glasses_AZ_Sunglasses1", 1 }, { "AuthenticZClothing.Glasses_AZ_Sunglasses2", 1 },
    { "Base.Hat_StrawHat", 1 }, { "Base.Hat_SummerHat", 1 },
    { "Base.Twine", 2 }, { "Base.RubberBand", 2 }, { "Base.DentalFloss", 2 },
    { "Base.Thread", 2 }, { "Base.Thread_Aramid", 2 }, { "Base.Thread_Sinew", 2 },
}

local function player0()
    local getter = rawget(_G, "getSpecificPlayer")
    if type(getter) == "function" then
        local ok, player = pcall(getter, 0)
        if ok and player then return player end
    end
    getter = rawget(_G, "getPlayer")
    if type(getter) == "function" then
        local ok, player = pcall(getter)
        if ok then return player end
    end
end

function TestKit.give(force)
    local player = player0()
    if not player or type(player.getInventory) ~= "function" or type(player.getModData) ~= "function" then
        return false, "local player unavailable"
    end
    if type(isClient) == "function" and isClient() then return false, "single-player only" end
    local inventory, data = player:getInventory(), player:getModData()
    if not inventory or type(inventory.AddItem) ~= "function" or not data then return false, "inventory unavailable" end
    -- Preserve the historical one-time grant without granting duplicate items.
    if data[MARKER] == nil and data["GlassesStayPut.TestKitVersion"] == VERSION then
        data[MARKER] = VERSION
    end
    if force ~= true and data[MARKER] == VERSION then
        print("[B47ANCEDEyewear][TestKit] Already granted; run B47ANCEDEyewearTestKit(true) to grant another.")
        return false, "already granted"
    end
    local granted, missing = 0, {}
    for _, entry in ipairs(CONTENTS) do
        for _ = 1, entry[2] do
            local ok, item = pcall(inventory.AddItem, inventory, entry[1])
            if ok and item then granted = granted + 1 else missing[#missing + 1] = entry[1] end
        end
    end
    data[MARKER] = VERSION
    print(string.format("[B47ANCEDEyewear][TestKit] Granted %d items; unavailable=%d.", granted, #missing))
    if #missing > 0 then print("[B47ANCEDEyewear][TestKit] Unavailable: " .. table.concat(missing, ", ")) end
    return true, { granted = granted, missing = missing }
end

function B47ANCEDEyewearTestKit(force)
    return TestKit.give(force == true)
end

print("[B47ANCEDEyewear][TestKit] Ready: B47ANCEDEyewearTestKit()")
return TestKit
