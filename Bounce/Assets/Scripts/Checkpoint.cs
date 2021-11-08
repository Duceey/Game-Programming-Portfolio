using UnityEngine;

public class Checkpoint : MonoBehaviour
{
    public GameObject Player;

    void OnTriggerEnter2D(Collider2D collider2D)
    {
        Player.GetComponent<PlayerMovement>().SetCheckpoint(transform);
    }
}
