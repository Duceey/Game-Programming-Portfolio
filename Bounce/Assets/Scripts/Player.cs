using UnityEngine;
using UnityEngine.UI;

public class Player : MonoBehaviour
{
    public float speed;
    public float rotationSpeed;

    public Transform lastCheckpoint;
    public Transform firstCheckpoint;

    private Rigidbody2D rb;

    void Start()
    {
        rb = GetComponent<Rigidbody2D>();
        LoadPlayer();
        Reset();
    }

    void Update()
    {
        // Player Rotational Movement
        Vector3 rotation = new Vector3(0, 0, -Input.GetAxisRaw("Horizontal") * rotationSpeed * Time.deltaTime);
        transform.Rotate(rotation);

        // Start Player
        if (rb.velocity == Vector2.zero && Input.GetKeyDown("space")) 
        { 
            rb.velocity = Direction() * speed;
            transform.GetChild(0).gameObject.SetActive(false);
        }

        // Reset Player
        if (Input.GetKeyDown("r")) { Reset(); }

        // Hard Reset Player
        if (Input.GetKeyDown("backspace")) { ResetPlayer(); }
    }

    void OnCollisionEnter2D(Collision2D collision2D)
    {
        if (collision2D.gameObject.layer == LayerMask.NameToLayer("Wall"))
        {
            Vector2 direction = Direction();
            Vector3 normal = collision2D.contacts[0].normal;

            if (Vector3.Angle(direction, normal) > 90)
            {
                rb.velocity = -direction * speed;
            }
            else if (Vector3.Angle(-direction, normal) > 90)
            {
                rb.velocity = direction * speed;
            }
            else { rb.velocity = normal * speed; }
        } 

        else if (collision2D.gameObject.layer == LayerMask.NameToLayer("Deathwall"))
        {
            Reset();
        } 

    }

    Vector2 Direction()
    {
        float angle = transform.localEulerAngles.z / 180 * Mathf.PI;

        return new Vector2(Mathf.Cos(angle), Mathf.Sin(angle));
    }

    void Reset()
    {
        rb.velocity = Vector2.zero;
        rb.position = lastCheckpoint.position;
        transform.GetChild(0).gameObject.SetActive(true);
    }

    public void SetCheckpoint(Transform checkpoint)
    {
        lastCheckpoint = checkpoint;
        SavePlayer();
    }

    public void SavePlayer()
    {
        SaveSystem.SavePlayer(this);
    }

    public void LoadPlayer()
    {
        PlayerData playerData = SaveSystem.LoadPlayer();

        rb.velocity = Vector2.zero;
        rb.position = new Vector3(playerData.position[0], playerData.position[1], playerData.position[2]);
        transform.GetChild(0).gameObject.SetActive(true);
    }

    public void ResetPlayer()
    {
        lastCheckpoint = firstCheckpoint;
        SavePlayer();
        Reset();
    }
}
