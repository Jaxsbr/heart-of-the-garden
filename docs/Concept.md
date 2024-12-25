# Heart of the Garden

## Concept

**Heart of the Garden** is a strategy-defense game where the player assumes the role of the Protector. The objective is to safeguard the Heart of the Garden from enemy attacks by using physical combat and strategic planting of protective plants. Players earn and spend game points to enhance gameplay by upgrading the Protector, the Heart, and the plants, tailoring their playstyle to their preferences.

---

## Player Profiles

Upon launching the game, players are greeted with a profile screen where they can:
- **Create a New Profile**: Provide a name and select a profile picture from a predefined list.
- **Select an Existing Profile**: Choose from a list of profiles displayed as `IMAGE | NAME`.

---

## Game Phases

### 1. Level Selection
Players progress through a journey of levels, starting with tutorials and beginner stages, advancing to more challenging levels.
- Levels vary in difficulty based on enemy types, attributes, spawn amounts, and terrain features.
- Levels are rated with 1 to 3 stars based on performance.
- Levels can be replayed to earn additional game points.
- Advanced levels are unlocked by completing preceding ones.

---

### 2. Game Point Usage
Game points shape the player’s strategy, enabling upgrades that focus on either strong defenses (plants) or a powerful Protector. Points are earned by:
- Completing levels.
- Reaching special milestones (e.g., deterring 1000 enemies).

#### Upgrade Options:
1. **Protector Abilities**:
   - Movement Speed
   - Watering Speed
   - Planting Speed
   - Courage (takes more damage before retreating)
   - Recovery Time (after being defeated)

2. **Heart Attributes**:
   - Maximum HP
   - Maximum Energy (for planting and repairs)
   - Energy Generation Rate
   - Resistance to enemy attack types (e.g., bite, burn, freeze)
   - Plant Growth Rate
   - Repair Energy Cost (varies by plant type and damage level)

3. **Plant Attributes**:
   - Maximum HP
   - Resistance to specific attacks
   - Thorn Damage (% chance to deter enemies)
   - Growth Rates (seedling → mature plant)
   - Unlockable Abilities:
     - New seedling types
     - Unique Protector abilities (e.g., jump, freeze, confuse enemies)

---

### 3. Gameplay

Each level begins with:
- A fully healed Heart.
- Starting energy levels.
- Enemy and wave configurations based on the level’s difficulty.

#### Objectives:
- Protect the Heart by planting defenses and confronting enemies.
- Use strategic upgrades to prepare for increasingly challenging enemy waves.

#### Mechanics:
- Enemy waves attack in increasing difficulty. Each wave:
  1. Targets the Heart.
  2. Destroys plants in its path.
  3. Engages the Protector if confronted.

- The Protector’s courage determines combat outcomes:
  - If defeated, the Protector retreats temporarily.
  - If victorious, enemies are deterred and flee.

#### Role of Plants:
Plants serve as defensive units with varying abilities:
- **Walling Plants**: Act as consumable barriers.
- **Damage Plants**: Inflict damage to deter enemies.
- **Effect Plants**: Impair or confuse enemies for a duration.

#### Role of the Heart:
- Passively grows plants from seedlings to maturity.
- Generates energy for planting and repairs.
- Does not deter enemies but serves as the core of defense.

#### Watering Mechanism:
- **Watering Needs**: Seedlings and young plants require water, while mature plants are sustained by the Heart.
- **Water Timer**: Each plant has an internal timer. When the timer elapses, a small watering icon appears above the plant.
- **Watering Action**:
  1. The Protector selects the watering can from the menu.
  2. The Protector identifies a plant needing water and moves to it.
  3. If the Protector has sufficient water units, the plant is watered directly. Otherwise, the Protector moves to a water tile to refill the watering can.
  4. The Protector’s water level indicator shows remaining water units.

#### Winning and Losing:
- **Win**: All enemy waves are deterred.
- **Lose**: The Heart is destroyed.

---

## Game Features

### Map and Navigation:
- **Tile Map**: Randomly generated terrain with rocks, soil, and water features.
- **Scrolling**: Navigate by moving the cursor near screen edges.
- **Mini-Map**: Toggleable for viewing enemies, collectables, and quick navigation.

### Planting:
- Select a seed from the menu if energy is available.
- A placement preview highlights valid tiles (green for valid, red for invalid).
- The Protector moves to the selected tile, executes a planting animation, and completes the task.

### Repairing:
- Select the repair option to preview repairable plants.
- Damaged plants are highlighted for repair (red indicates invalid or unnecessary repairs).

---

### Enemy Waves
- **Wave Announcements**: Countdown before waves begin (e.g., "Wave 1 starting in 30 seconds").
- **Wave Configurations**: Based on level difficulty, with increasing enemy variety and spawn rates.
- **Wave End Conditions**:
  - All enemies are deterred.
  - The Heart is destroyed.

---

## Level Completion

After the final wave:
- **Win**: A level completion screen displays the star rating and game points earned.
- **Loss**: The level over screen explains what went wrong, encouraging a retry.
