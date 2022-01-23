using UnityEngine;

public class Checkpoint : MonoBehaviour
{
    void OnTriggerEnter2D(Collider2D collider2D)
    {
        if (collider2D.CompareTag("Player"))
        {
            collider2D.gameObject.GetComponent<Player>().SetCheckpoint(transform);
        }
    }
}
