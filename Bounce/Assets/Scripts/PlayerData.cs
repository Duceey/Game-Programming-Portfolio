using UnityEngine;

[System.Serializable]
public class PlayerData
{
    public float[] position;

    public PlayerData (Player player)
    {
        position = new float[3];
        position[0] = player.lastCheckpoint.position.x;
        position[1] = player.lastCheckpoint.position.y;
        position[2] = player.lastCheckpoint.position.z;
    }
}
